
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Project Model 

class Project(models.Model):
    project_id = models.PositiveIntegerField(primary_key=True)
    type_choices = (("Residential", "Residential"), ("Commercial", "Commercial"))
    type_of_project = models.CharField(max_length=50, choices=type_choices)
    name_of_property = models.CharField(max_length=100)
    bhk_choices = (("1BHK", "1BHK"), ("2BHK", "2BHK"), ("3BHK", "3BHK"),("4BHK", "4BHK"))
    no_of_bhk = models.CharField(max_length=10, choices=bhk_choices)
    area_of_property_located = models.CharField(max_length=20)
    description = models.TextField()
    amenities = models.TextField()
    price = models.FloatField()
    negotiable_choices = (("Yes", "Yes"), ("No", "No"))
    negotiable = models.CharField(max_length=50, choices=negotiable_choices)
    display_image=models.ImageField(upload_to="projects/display_image/",null=True,default=None)

    def __str__(self):
        return self.name_of_property


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/images/")

    def __str__(self):
        return f"Image for {self.project.name_of_property}"

# Upcoming Project Model

class Upcoming(models.Model):
    upcoming_project_id = models.PositiveIntegerField(primary_key=True)
    type_choices = (("Residential", "Residential"), ("Commercial", "Commercial"))
    type_of_project = models.CharField(max_length=50, choices=type_choices)
    name_of_project = models.CharField(max_length=100)
    bhk_choices = (("1BHK", "1BHK"), ("2BHK", "2BHK"), ("3BHK", "3BHK"),("4BHK", "4BHK"))
    no_of_bhk = models.CharField(max_length=10, choices=bhk_choices)
    area_of_project_located = models.CharField(max_length=20)
    builder_name = models.CharField(max_length=50)
    description = models.TextField()
    amenities = models.TextField()
    rera_no = models.CharField(max_length=50)
    total_area_of_project = models.CharField(max_length=50)
    floor_plan=models.FileField(upload_to="files", null=True, default=None)
    brochure=models.FileField(upload_to="files", null=True, default=None)
    display_image=models.ImageField(upload_to="upcoming/display_image/",null=True,default=None)

    def __str__(self):
        return self.name_of_project


class UpcomingImage(models.Model):
    upcoming_project = models.ForeignKey(Upcoming, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="upcoming/images/")

    def __str__(self):
        return f"Image for {self.upcoming_project.name_of_project}"


# Appointment Model
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    service_name = models.CharField(max_length=100)  
    service_description = models.TextField()  
    service_fee = models.DecimalField(max_digits=8, decimal_places=2)  
    date = models.DateTimeField()  
    phone = models.CharField(max_length=10) 
    email = models.EmailField()  
    message = models.TextField()

    def __str__(self):
        return f"{self.service_name} appointment with {self.user.username} on {self.date}"


#  Contact Model    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"