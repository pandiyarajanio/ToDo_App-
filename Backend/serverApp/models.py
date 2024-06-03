from django.db import models

class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name