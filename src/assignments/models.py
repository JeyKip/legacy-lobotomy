from django.db import models, IntegrityError, transaction
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from app.utils import upload_image_path, upload_video_path, content_types
from .validators import validate_max_age, validate_min_age, FileValidator

from users.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255, unique=True, null=False,
                            blank=False)

    def __str__(self):
        return self.name


class AssingmentTarget(models.Model):
    class Meta:
        verbose_name = 'Target'

    name = models.CharField(max_length=255, unique=True, null=False,
                            blank=False)
    min_age = models.PositiveSmallIntegerField(default=13, null=True,
                                               blank=True,
                                               validators=[validate_min_age, ])
    max_age = models.PositiveSmallIntegerField(default=99, null=True,
                                               blank=True)
    male = models.BooleanField(default=False, help_text='Assign to all males')
    female = models.BooleanField(default=False,
                                 help_text='Assign to all females')
    non_binary = models.BooleanField(default=False,
                                     help_text='Assign to all non-binaries')
    transgender = models.BooleanField(default=False,
                                      help_text='Assign to all transgenders')
    other = models.BooleanField(default=False,
                                help_text='Assign to all others')
    law_explorer = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.min_age > self.max_age:
            raise ValidationError('Min age should be less or equal to max age')


class Assignment(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False,
                            blank=False)
    description = models.TextField(null=True, blank=False)
    image = models.ImageField(upload_to=upload_image_path, null=True,
                              blank=False, verbose_name='Tile Image',
                              default='assignments/images/default.jpeg')
    points = models.PositiveIntegerField(blank=False, null=True)
    time = models.PositiveIntegerField(blank=True, null=True,
                                       help_text='Time in seconds')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True,
                                 blank=False)

    target = models.ForeignKey(AssingmentTarget, on_delete=models.PROTECT,
                               related_name='target', null=True)
    priority = models.IntegerField(default=0)
    dependent_on = models.ForeignKey('self', null=True, blank=True,
                                     on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AssignmentBlock(models.Model):
    TYPE_CHOICES = (
        ('Text', 'Text'),
        ('Image', 'Image'),
        ('Video', 'Video'),
        ('Question', 'Question'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    type_of_block = models.CharField(max_length=32, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,
                                   related_name='blocks')


class TextBlock(models.Model):
    block = models.OneToOneField(AssignmentBlock, on_delete=models.CASCADE,
                                 related_name='text')

    text = models.TextField(blank=True)


class ImageBlock(models.Model):
    block = models.OneToOneField(AssignmentBlock, on_delete=models.CASCADE,
                                 related_name='image')
    image = models.ImageField(upload_to=upload_image_path, blank=True)


class VideoBlock(models.Model):
    block = models.OneToOneField(AssignmentBlock, on_delete=models.CASCADE,
                                 related_name='video')
    video = models.FileField(upload_to=upload_video_path, blank=True,
                             validators=[FileValidator(
                                 content_types=content_types)])


class QuestionBlock(models.Model):
    block = models.OneToOneField(AssignmentBlock, on_delete=models.CASCADE,
                                 related_name='question')
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.TextField(blank=False)
    tip = models.TextField(blank=True)
    is_correct = models.BooleanField(blank=False)
    question = models.ForeignKey(QuestionBlock, on_delete=models.CASCADE,
                                 related_name='options')

    def clean(self):
        if self.is_correct:
            correct_answer = Option.objects.filter(
                ~Q(pk=self.pk),
                question=self.question,
                is_correct=True).count()
            if correct_answer > 0:
                raise ValidationError(
                    "Only one correct answer per question"
                )


class UserAssignment(models.Model):
    class Meta:
        unique_together = ['user', 'assignment']

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True)

    def locked(self):
        if self.assignment.dependent_on:
            try:
                dependent = UserAssignment.objects.get(
                    assignment_id=self.assignment.dependent_on.id,
                    user=self.user
                )
                if not dependent.is_completed:
                    return True
            except UserAssignment.DoesNotExist:
                return False
        return False

    def __str__(self):
        return f'{self.user.email} - {self.assignment.name}'


def reassign(assignment_instance, user_instance):
    if assignment_instance.target is not None:
        target_genders = []
        if assignment_instance.target.male:
            target_genders.append('Male')
        if assignment_instance.target.female:
            target_genders.append('Female')
        if assignment_instance.target.non_binary:
            target_genders.append('Non-Binary')
        if assignment_instance.target.transgender:
            target_genders.append('Transgender')
        if assignment_instance.target.other:
            target_genders.append('Other')

        target_activities = []
        if assignment_instance.target.law_explorer:
            target_activities.append('Law Explorers')
        if not target_activities:
            target_activities.append(None)

        if assignment_instance.target.min_age <= user_instance.age <= assignment_instance.target.max_age \
                and user_instance.gender in target_genders \
                and (user_instance.activity in target_activities):
            try:
                with transaction.atomic():
                    UserAssignment.objects.create(user=user_instance,
                                                  assignment_id=assignment_instance.id)
            except IntegrityError:
                pass


@receiver(post_save, sender=Assignment)
def assign_changed_assignment(sender, instance, created, **kwargs):
    for userassignment in UserAssignment.objects.filter(
            assignment_id=instance.id):
        if not userassignment.is_completed:
            userassignment.delete()

    for user in User.objects.all():
        reassign(assignment_instance=instance, user_instance=user)


@receiver(post_save, sender=User)
def assign_to_changed_user(sender, instance, created, **kwargs):
    for userassignment in UserAssignment.objects.filter(
            user__id=instance.id):
        if not userassignment.is_completed:
            userassignment.delete()

    for assignment in Assignment.objects.all():
        reassign(assignment_instance=assignment, user_instance=instance)


@receiver(post_save, sender=AssingmentTarget)
def assign_changed_target(sender, instance, created, **kwargs):
    for userassignment in UserAssignment.objects.filter(
            assignment__target_id=instance.id):
        if not userassignment.is_completed:
            userassignment.delete()

    for assignment in Assignment.objects.filter(
            category__assignment__target=instance):
        for user in User.objects.all():
            reassign(assignment_instance=assignment, user_instance=user)


# prevents from saving empty blocks
@receiver(post_save, sender=AssignmentBlock)
def prevent_empty_blocks(sender, instance, created, **kwargs):
    if not any(hasattr(instance, attr) for attr in
               ['text', 'video', 'image', 'question']):
        if instance.name != 'BULK_UPLOAD':
            instance.delete()
