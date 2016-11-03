from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    THEMES = (
        ('1', 'Cosmo'),
        ('2', 'Darkly'),
        ('3', 'Superhero'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=1, default=THEMES[0], choices=THEMES)

    class Meta:
        app_label = 'jam'

    def theme_name(self):
        for key, name in self.THEMES:
            if key == self.theme:
                return name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
