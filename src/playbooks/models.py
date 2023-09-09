from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from app.utils import upload_image_path, upload_video_path

from users.models import User

from assignments.models import Category


class PlaybookAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True,
                              blank=False)
    points = models.PositiveIntegerField(blank=False, null=True)
    time = models.PositiveIntegerField(blank=False, null=True,
                                       help_text='Time in seconds')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True,
                                 blank=False)
    priority = models.IntegerField(default=0)
    dependent_on = models.ForeignKey('self', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    completed = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class PlaybookAssignmentBlock(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type_of_block = models.CharField(max_length=32, blank=True)
    assignment = models.ForeignKey(PlaybookAssignment, on_delete=models.CASCADE,
                                   related_name='blocks')


class PlaybookTextBlock(models.Model):
    block = models.OneToOneField(PlaybookAssignmentBlock, on_delete=models.CASCADE,
                                 related_name='text')

    text = models.TextField(blank=True)


class PlaybookImageBlock(models.Model):
    block = models.OneToOneField(PlaybookAssignmentBlock, on_delete=models.CASCADE,
                                 related_name='image')
    image = models.ImageField(upload_to=upload_image_path, blank=True)


class PlaybookVideoBlock(models.Model):
    block = models.OneToOneField(PlaybookAssignmentBlock, on_delete=models.CASCADE,
                                 related_name='video')
    video = models.FileField(upload_to=upload_video_path, blank=True)


class PlaybookQuestionBlock(models.Model):
    block = models.OneToOneField(PlaybookAssignmentBlock, on_delete=models.CASCADE,
                                 related_name='question')
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text


class PlaybookOption(models.Model):
    text = models.TextField(blank=False)
    tip = models.TextField(blank=True)
    is_correct = models.BooleanField(blank=False)
    question = models.ForeignKey(PlaybookQuestionBlock, on_delete=models.CASCADE,
                                 related_name='options')

    def __str__(self):
        return self.text


@receiver(post_save, sender=PlaybookAssignment)
def calculate_total_points(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.user.pk)
        user.total_points += instance.points
        user.save()
