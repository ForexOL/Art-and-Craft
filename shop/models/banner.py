from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    other_details = models.JSONField(blank=True, null=True)  # Stores extra details as JSON
    image =models.ImageField(upload_to='Uploads/banner/', blank=True)
    def __str__(self):
        return self.title
 