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
        fields = ('order_number', 'user', 'delivery_man_id', 'delivery_man', 'total_amount', 'delivery_address', 'status', 'created_at', 'updated_at')
        read_only_fields = ('order_number','user', 'created_at', 'updated_at')

    
    # def validate(self, data):
    #     user = self.context['request'].user
    #     instance = self.instance  

    #     if instance and 'delivery_man' in data:
    #         if user.role != User.Role.ADMIN:
    #             raise serializers.ValidationError({
    #                 'delivery_man': 'Only admin can change delivery man.'
    #             })

    #     if instance and 'status' in data:
    #         if user.role != User.Role.DELIVERY_MAN:
    #             raise serializers.ValidationError({
    #                 'status': 'Only delivery man can update order status.'
    #             })

    #     return data

    # def update(self, instance, validated_data):
    #     if 'delivery_man' in validated_data:
    #         if self.context['request'].user.role != User.Role.ADMIN:
    #             validated_data.pop('delivery_man')

    #     if 'status' in validated_data:
    #         if self.context['request'].user.role != User.Role.DELIVERY_MAN:
    #             validated_data.pop('status')

    #     return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeliveryOrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status'] 