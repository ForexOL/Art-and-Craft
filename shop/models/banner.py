from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    other_details = models.JSONField(blank=True, null=True)  # Stores extra details as JSON

    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.title
