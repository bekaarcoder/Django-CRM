from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
  pass


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Lead(models.Model):

  # SOURCE_CHOICES = (
  #   ('YouTube', 'YouTube'),
  #   ('Google', 'Google'),
  #   ('Newsletter', 'Newsletter')
  # )

  # phoned = models.BooleanField(default=False)
  # source = models.CharField(choices=SOURCE_CHOICES, max_length=100)
  # profile_picture = models.ImageField(blank=True, null=True)
  # special_files = models.FileField()

  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  age = models.IntegerField(default=0)
  agent = models.ForeignKey("Agent", on_delete=models.CASCADE)


class Agent(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.email

  
def post_user_created_signal(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)