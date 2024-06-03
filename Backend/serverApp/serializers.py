from rest_framework import serializers
from .models import Todo

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'created_at', 'updated_at']