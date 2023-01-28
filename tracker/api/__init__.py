from rest_framework import serializers
from ..models import User
 
class UserSerializer(serializers.ModelField):
    class Meta:
        model=User
        fields=['username','email',]