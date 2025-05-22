from django.contrib import admin
from .models import Project, ProjectImage, Upcoming, UpcomingImage, Appointment, ContactMessage

# Inline model for ProjectImage
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  

class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "project_id",
        "type_of_project",
        "name_of_property",
        "no_of_bhk",
        "area_of_property_located",
        "description",
        "amenities",
        "price",
        "negotiable",
    ]
    inlines = [ProjectImageInline]

admin.site.register(Project, ProjectAdmin)

# Inline model for UpcomingImage
class UpcomingImageInline(admin.TabularInline):
    model = UpcomingImage
    extra = 1  

class UpcomingAdmin(admin.ModelAdmin):
    list_display = [
        "upcoming_project_id",
        "type_of_project",
        "name_of_project",
        "no_of_bhk",
        "area_of_project_located",
        "builder_name",
        "description",
        "amenities",
        "rera_no",
        "total_area_of_project",
    ]
    inlines = [UpcomingImageInline]

admin.site.register(Upcoming, UpcomingAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
    "user",
    "service_name",
    "service_description",
    "service_fee",
    "date",
    "phone",
    "email",
    "message",
    ]

admin.site.register(Appointment, AppointmentAdmin)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')
