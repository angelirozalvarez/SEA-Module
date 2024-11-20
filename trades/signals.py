from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_staff_to_admin_group(sender, instance, created, **kwargs):
    if instance.is_staff:
        admin_group, created = Group.objects.get_or_create(name="Admin")
        instance.groups.add(admin_group)
