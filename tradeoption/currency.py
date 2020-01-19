from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return self.code
