from rest_framework import serializers
from django.contrib.auth import get_user_model
from tracker.models import Application,Customer,Admin,Level
from django.db import IntegrityError
User= get_user_model()



class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
   
    class Meta:
        model=User
        fields= ['email','phone_no','password','is_admin','fullname','created_at','updated_at']

    def validate(self,attrs):
       
        phone_no =attrs.get('phone_no','')
        
        if not phone_no.isnumeric():
            raise serializers.ValidationError('Phone number should contain only numbers')
        return attrs

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user




class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    first_name=serializers.CharField(write_only=True)
    last_name=serializers.CharField(write_only=True)
    email=serializers.EmailField(write_only=True)
    phone_no=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Admin
        fields=[
            'user',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_no',
            'role'

        ]
    def create(self,validated_data):
        user_inst=User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_no=validated_data['phone_no']
            )
        return Admin.objects.create(
            user=user_inst,
            role=validated_data['role']
        )
        

class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    fullname=serializers.CharField(write_only=True)
    email=serializers.EmailField(write_only=True)
    phone_no=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model=Customer
        fields=[
            'user',
            'password',
           'fullname',
            'email',
            'phone_no'
            
        ]
        extra_kwargs={'reg_num':{'read_only':True}}

    def create(self,validated_data):
        try:
            user_inst=User.objects.create(

       
                fullname=validated_data['fullname'],
                email=validated_data['email'],
                phone_no=validated_data['phone_no']
                )
            
            user_inst.set_password(validated_data['password'])
            user_inst.save()
            customer=Customer.objects.create(
            user=user_inst
            )
        
        except IntegrityError:
            raise serializers.ValidationError("user already exists")

        return customer

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields='__all__'    

class ApplicationSerializer(serializers.ModelSerializer):
    user=CustomerSerializer(read_only=True)
    level=LevelSerializer(read_only=True)
    
    
    class Meta:
        model=Application
        fields="__all__"
        # extra_kwargs={'user':{'read_only':True}}

    def create(self, validated_data):
        is_customer=hasattr(validated_data['user'],'customer')
        if not is_customer:
            raise serializers.ValidationError('Admin cannot create Application, login as User')



        level_obj=Level.objects.create(stage='stage 1',status=False,current_level=True)
        
        app=Application.objects.create(
        # user=validated_data['user'],
        level=level_obj,


        user=validated_data['user'].customer,


        age=validated_data['age'],
        birth_certificate=validated_data['birth_certificate'],
        nationality=validated_data['nationality'],
        state_of_origin=validated_data['state_of_origin'],
        occupation=validated_data['occupation'],
        site_LGA=validated_data['site_LGA'],
        post_held=validated_data['post_held'],
        address=validated_data['address'],
        business_reg_cert=validated_data['business_reg_cert'],
        business_reg_name=validated_data['business_reg_name'],
        business_reg_num=validated_data['business_reg_num'],
        business_reg_year=validated_data['business_reg_year'],
        agent_name=validated_data['agent_name'],
        agent_address=validated_data['agent_address'],
        specific_purpose_of_land=validated_data['specific_purpose_of_land'],
        plot_no=validated_data['plot_no'],
        block_no=validated_data['block_no'],
        street_no=validated_data['street_no'],
        underdeveloped=validated_data['underdeveloped'],
        minning=validated_data['minning'],
        purpose_of_land=validated_data['purpose_of_land'],
        development_proposal=validated_data.get('development_proposal',''),
        amount=validated_data['amount'],
        use=validated_data['use'],
        
        )
        app.save()
        return app



     
        