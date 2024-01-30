from rest_framework import serializers
from .models import *


class CheckUserSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        user_name = data.get('username')

        if user_name:
            
            user = CustomUser.objects.filter(email=user_name)
            if not user:
                raise serializers.ValidationError({'status':'False','error':'Invalid Username.'})
        else:
            raise serializers.ValidationError({'error':'User Name are required.'})
        
        data['user'] = user
        return data

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['user_name',
            'phone_number',
            'meessage',
            'message_file']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.user_name.email
        return representation
    
    def to_internal_value(self,data):
        try:
            user = data.get("user_name")
            if user:
                user = CustomUser.objects.get(email=user)
                data['user_name'] = user.id
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error':'User is not exists.'})
        return super().to_internal_value(data)
    
    def create(self,validated_data):
        user_names  = validated_data['user_name']
        phone_numbers =  validated_data['phone_number']
        meessages = validated_data.get('meessage',"")
        message_files = validated_data.get('message_file',"")
        if not meessages and not message_files:
            raise serializers.ValidationError({'error':'Either a message or files are required.'})
        create_machine = MessageModel.objects.create(
            user_name = user_names,
            phone_number = phone_numbers,
            meessage = meessages,
            message_file = message_files
        )
        return create_machine

