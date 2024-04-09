# projects/serializers.py
from rest_framework import serializers
from .models import Project, ProjectMembership
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Adjust fields based on your User model
        fields = ['id', 'username', 'email']


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='user')

    class Meta:
        model = ProjectMembership
        fields = ['user', 'user_id', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    users = ProjectMembershipSerializer(
        source='projectmembership_set', many=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        users_data = validated_data.pop('projectmembership_set', [])
        project = Project.objects.create(**validated_data)
        for user_data in users_data:
            ProjectMembership.objects.create(project=project, **user_data)
        return project

    def update(self, instance, validated_data):
        users_data = validated_data.pop('projectmembership_set', [])
        project = super().update(instance, validated_data)
        for user_data in users_data:
            user_id = user_data.pop('user').id
            ProjectMembership.objects.update_or_create(
                project=project, user_id=user_id, defaults=user_data)
        return project
