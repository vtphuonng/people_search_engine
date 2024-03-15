from django.db import models

class BasicInformation(models.Model):
    personorder = models.IntegerField(primary_key=True)
    identity_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=45)
    sex = models.CharField(max_length=1)
    dob = models.DateField()
    nationality = models.CharField(max_length=45)
    place_of_origin = models.TextField()
    place_of_resident = models.TextField()
    personal_id = models.TextField()
    id_date = models.DateField()
    provider = models.TextField()

class ContactInfo(models.Model):
    id_number = models.IntegerField(primary_key=True)
    phone = models.BigIntegerField(null=True)
    gmail = models.EmailField(null=True)
    used_platforms = models.IntegerField(null=True)

class SocialNetworkProfile(models.Model):
    id = models.AutoField(primary_key=True)
    personal_used_sp = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    platform = models.ForeignKey('SocialPlatforms', on_delete=models.CASCADE)
    account_server = models.ForeignKey('SocialPlatformServer', on_delete=models.CASCADE)
    account = models.TextField()
    pass_field = models.TextField()

class SocialPlatformServer(models.Model):
    id = models.AutoField(primary_key=True)
    server_region = models.TextField()

class SocialPlatforms(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platforms = models.CharField(max_length=45)