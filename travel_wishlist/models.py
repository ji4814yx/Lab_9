from django.db import models


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

# Add a string method
    def __str__(self):
        return f'{self.name} visited? {self.visited}'  # this is going to be displayed
        # to the user in the admin console
