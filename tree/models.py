from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)


# Individual-specific data
class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()

# College student-specific data
class College(models.Model):
    name = models.CharField(max_length=100)

class CollegeStudent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    # college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    college=models.TextField()

# Industry/organization-specific data
class IndustryOrganization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    organization_name = models.CharField(max_length=100)

