from django.db import models

class CurrentQuery(models.Model):
    fbId = models.TextField(primary_key=True)
    queryId = models.TextField(null=True, default=None)
