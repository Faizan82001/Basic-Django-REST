from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "password", "created_at", "phone_number", "gender"]
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        user = Customer.objects.create(email=validated_data['email'], name=validated_data['name'], phone_number=validated_data['phone_number'], gender=validated_data['gender'])
        user.set_password(validated_data['password'])
        user.save()
        return user