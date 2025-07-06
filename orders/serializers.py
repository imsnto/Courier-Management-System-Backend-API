from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Order

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']



class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_man_id = serializers.PrimaryKeyRelatedField(
        source='delivery_man',
        queryset=User.objects.filter(role=User.Role.DELIVERY_MAN),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = ('id', 'user', 'product', 'quantity', 'delivery_man_id', 'delivery_man', 'delivery_address', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id','user', 'created_at', 'updated_at')


    
    def create(self, validated_data):
        if self.context['request'].user.role == 'DELIVERY_MAN':
            raise serializers.ValidationError("Delivery man cannot create orders.")
        
        if self.context['request'].user.role == 'USER' and 'status' in validated_data:
            validated_data['status'] = Order.Status.PENDING
        
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    


class DeliveryOrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status'] 


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'quantity', 'product', 'delivery_address',  'status', 'created_at']
        read_only_fields = ['id', 'created_at']