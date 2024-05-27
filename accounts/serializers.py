from rest_framework import serializers
from .models import CustomUser, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """
      The UserSerializer class is a serializer for the CustomUser model,
      handling the serialization and deserialization of user data,
      including sensitive information like passwords which are write-only.

      Example Usage
      # Creating a new user instance via the serializer
      user_data = {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'mobile': '1234567890',
        'email': 'john@example.com',
        'password': 'securepassword123'
      }
      user_serializer = UserSerializer(data=user_data)
      if user_serializer.is_valid():
    user = user_serializer.save()
    print(user.id)  # Outputs the ID of the newly created user

    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            mobile=validated_data["mobile"],
        )
        user.set_password(validated_data["password"])
        user.is_active = False  # User must verify email before activating
        user.save()
        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    This Serializes instances of the FriendRequest model to JSON.
    Handles read-only serialization of user data involved in the friend request using nested UserSerializer.
    """

    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "status", "timestamp"]
