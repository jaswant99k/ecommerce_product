from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import re

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    username = serializers.CharField(write_only=True,required=False,)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'token',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        if user.email:
            user.username = user.email
        else:
            user.username = user.mobile
        user.save()
        return user

    def get_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                u'This email address already exist.')
        return value

    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        
        username = data['username']
        print(username)
        user = authenticate(**data)
        #if user and user.is_active:
        if user:
            return user
        else:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username):
                try:
                    user_by_email = User.objects.get(email=username).username
                    data['username']=user_by_email
                    user = authenticate(**data)
                    if user:
                        return user
                except:
                    raise serializers.ValidationError("Incorrect Credentials")
            else:
                try:
                    user_by_mobile = User.objects.get(mobile=username).username
                    print(user_by_mobile)
                    data['username']=user_by_mobile
                    print(data)
                    user = authenticate(**data)
                    if user:
                        return user
                except Exception as e:
                    
                    print(e.message)
                    raise serializers.ValidationError("Incorrect Credentials")

        raise serializers.ValidationError("Incorrect Credentials")


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True,required=False,)
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CheckPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
