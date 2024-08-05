from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProgramaLealtad

@receiver(post_save, sender=User)
def create_user_points(sender, instance, created, **kwargs):
    if created:
        ProgramaLealtad.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_points(sender, instance, **kwargs):
    instance.programaLealtad.save()
