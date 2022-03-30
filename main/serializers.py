
from dataclasses import fields
from rest_framework import serializers
from .models import  User ,UserProfile  ,TypesBikes ,Accessories ,BikeDetails #, IP
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

# NOTE : serialize mean to convert object to an understand format or data type
# if you want to include model here user serializer.Serialize

class UserSerializer( serializers.ModelSerializer ) : 
    class Meta :
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'age', 'gender')



class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True }}


    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            age=profile_data['age'],
            # address= profile_data
            gender=profile_data['gender']
        )
        return user





JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer( serializers.Serializer ): # here we include ith models dtype
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }



class TypeBikeSerializer( serializers.ModelSerializer ) :
    class Meta:
        model = TypesBikes
        fields = '__all__'

class Itemserializer ( serializers.ModelSerializer ) :
    #image       = serializers.)
    #specs       = serializers.FileField(db_index=True , upload_to='specs')
    # cycle_name  = serializers.CharField(max_length=100)
    # descriptive = serializers.CharField(required=False, max_length=100)
    # cycle       = serializers.CharField(max_length=100)
    # price       = serializers.FloatField()
    #serialized_store = StoreSerializer(store, context={"request": request})
    # Allow image url 
    photo_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta :  # A metaclass in Python is a class of a class that defines how a class behaves
        model = BikeDetails
        fields = '__all__'
        # exclude = ['']

        
class Accserializer ( serializers.ModelSerializer ) :
    photo_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta :  # A metaclass in Python is a class of a class that defines how a class behaves
        model = Accessories
        fields = '__all__'

        # exclude = ['']


# class IPSerializer( serializers.ModelSerializer ) :
#     class Meta:
#         model = IP
#         fields = '__all__'



