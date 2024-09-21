from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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


from django.db import models
from django.contrib.auth.models import User

class TreePlan(models.Model):
    PLAN_CHOICES = [
        (1, '1'),
        (2, '5'),
        (3, '10'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price field
    number_of_trees = models.IntegerField(choices=PLAN_CHOICES)
    
    def __str__(self):
        return f'{self.name} - {self.number_of_trees} Trees'

class Tree(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tree_plan = models.ForeignKey(TreePlan, on_delete=models.SET_NULL, null=True, blank=True)  # Link to TreePlan
    name = models.CharField(max_length=255)
    number_of_trees = models.IntegerField()
    date_planted = models.DateField()
    location = models.CharField(max_length=255)  # To integrate with Google Maps API
    photo = models.ImageField(upload_to='tree_photos/')
    video = models.FileField(upload_to='tree_videos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} planted by {self.user}"


