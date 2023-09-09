from django.db import models

from users.models import User


class TermsAndConditions(models.Model):
    class Meta:
        verbose_name_plural = 'Terms and Conditions'

    text = models.TextField(null=True, blank=False)

    def __str__(self):
        return 'Terms and Conditions'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        for user in User.objects.all():
            user.accepted_terms_cond = False
            user.save()

        super(TermsAndConditions, self).save(
            force_insert, force_update, using, update_fields)
