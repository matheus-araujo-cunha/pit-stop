from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "is_superuser", "password"]
        read_only_fields = ["id", "is_superuser"]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        try:
            user_authenticated = self.context["request"].user.name
            user_admin = self.context["request"].user.is_superuser
            if user_admin:
                return User.objects.create_superuser(**validated_data)
            return User.objects.create_user(**validated_data)
        except AttributeError:
            return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
