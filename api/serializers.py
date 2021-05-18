from rest_framework import serializers
from .models import User, employee, department
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'password']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  department
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id')

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None :
            raise serializers.ValidationError(
                'Username is required to log in.'
            )
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'We could not find a user with this username and password. Please try again.'
            )

        return user.pk


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all())] )
    email = serializers.EmailField()
    password = serializers.CharField(required=True, validators=[validate_password])
    name = serializers.CharField()
    join = serializers.DateField()
    dob = serializers.DateField(required=False)
    phone = serializers.CharField(max_length=10, min_length=10, allow_null=True, allow_blank=True)
    dept = serializers.IntegerField()
    address = serializers.CharField( allow_null=True, allow_blank=True)


'''
class RegisterSerializer(serializers.ModelSerializer):
    username =
    email = serializers.EmailField( write_only=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    token = serializers.CharField(max_length=255, read_only=True)
    name = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = NewUser
        fields = ('pk', 'name', 'email', 'password')
        extra_kwargs = {
            'name': {'required': True},
        }
        read_only_fields = ('pk')

    def create(self, validated_data):
        user = NewUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
'''