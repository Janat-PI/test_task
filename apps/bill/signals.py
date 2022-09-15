from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Card, Client


@receiver(post_save, sender=Client)
def create_card_signal(sender, instance, created, **kwargs):
    if created:
        Card.objects.create(
            client=instance
        )