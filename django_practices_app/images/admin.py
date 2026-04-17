from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'image_url', 'upload_date', 'is_active']

# Register your models here.
