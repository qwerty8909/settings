from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True)
    named_url = models.CharField(max_length=255, blank=True)
    menu = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        else:
            return self.url
