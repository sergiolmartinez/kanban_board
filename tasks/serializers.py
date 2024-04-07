from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('owner',)  # Mark 'owner' as a read-only field

    def create(self, validated_data):
        # Set the 'owner' to the current user during task creation
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
