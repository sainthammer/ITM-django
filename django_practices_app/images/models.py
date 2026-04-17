from django.db import models

class Image(models.Model):
    image_name = models.CharField(max_length=100, unique=True)
    image_url = models.ImageField(upload_to="images/", unique=True)
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name
