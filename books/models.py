from django.db import models
    
class Book(models.Model):
    name = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description
