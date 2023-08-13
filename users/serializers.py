from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        #set an option for the password to make it write only, meaning that it will not be shown is json object after posting register fields to our api
        extra_kwargs = {
            'password': {'write_only': True}
        }

    #overwrite the default create function to hash the password
    def create(self, validated_data): #validated_data means that all fiels are provided
        password = validated_data.pop('password', None) #extract the password
        instance = self.Meta.model(**validated_data) #create the user instance, with the validated data without the extracted password
        if password is not None:
            instance.set_password(password) #set_password function is provided by django and it will hash the password for us
        instance.save()
        return instance