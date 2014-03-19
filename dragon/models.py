from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
     # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)
    # picture = models.ImageField(upload_to='profile_images', blank=True)
    # Override the __unicode__() method to return out something meaningful!
    age = models.IntegerField(default=0)
    gender=models.CharField(max_length=10)
    educationLevel= models.CharField(max_length=40)
    firstLanguage=models.CharField(max_length=20,null=True)

    def __unicode__(self):
        return self.user.username

class Experiment(models.Model):
    userId = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=128,unique=True)
    payment=models.IntegerField()
    description=models.CharField(max_length =5000)
    educationDemand=models.CharField(max_length=20,null=True)
    language=models.CharField(max_length=40,null=True)
    startTime=models.DateField()
    endTime=models.DateField()
    maxPosition=models.IntegerField()
    currentOffer=models.IntegerField(default=0)
    isOverdue=models.BooleanField(default=True)
    def __unicode__(self):
        return self.title

class ApplyRecord(models.Model):
    applicantId = models.ForeignKey(UserProfile)
    experimentId= models.ForeignKey(Experiment)
    ApplyTime = models.DateField()
    isProcessed=models.BooleanField(default=True)
    isOffered = models.BooleanField(default=False)
    isAccepted = models.BooleanField(default=False)
    isValid = models.BooleanField(default=True)