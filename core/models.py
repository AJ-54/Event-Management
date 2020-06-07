from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator
import os

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.name, str(instance.token)+'-'+filename)

class Candidate(models.Model):

    CHOICES = (
        ("SELF","Self"),
        ("GROUP","Group"),
        ("CORPORATE","Corporate"),
        ("OTHERS","Others"),
    )
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, blank=True)
    email = models.EmailField(max_length=150)
    proof = models.FileField(upload_to=user_directory_path)
    org = models.CharField(max_length=20, choices=CHOICES, default='SELF')
    ticket = models.IntegerField(default=1)
    token = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# To delete the resume after each application is deleted.
@receiver(post_delete, sender=Candidate)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.proof:
        if os.path.isfile(instance.proof.path):
            os.remove(instance.proof.path)