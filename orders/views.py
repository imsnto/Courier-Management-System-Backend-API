from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer, DeliveryOrderUpdateSerializer
from .permissions import IsOrderOwnerOrAdmin


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin]

    def get_queryset(self, request):
        user = request.user
        if user.role == 'USER':
            orders = Order.objects.filter(user=user)
        elif user.role == 'ADMIN':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(delivery_man=user)   
        return orders
    
    
    def list(self, request):
        orders = self.get_queryset(request)
        if not orders:
            return Response({"message": "No orders found"}, status=404)
        
        return Response(OrderSerializer(orders, many=True).data)

    def retrieve(self, request, pk=None):        
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=404)

        self.check_object_permissions(request, order)
        return Response(OrderSerializer(order).data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=404)

        if request.user.role != 'ADMIN' and request.user.role != 'DELIVERY_MAN':
            return Response({"message": "You do not have permission to update this order"}, status=403)

        if request.user.role == 'DELIVERY_MAN':
            serializer = DeliveryOrderUpdateSerializer(order, data=request.data, partial=True, context={'request': request})
        else:
            serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=400)

    
