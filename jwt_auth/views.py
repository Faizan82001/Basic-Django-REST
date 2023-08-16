from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer
from .models import Customer
from pizza.models import Order
from pizza.serializers import OrderSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Import the permission
    

class RegistrationView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User Created Successfully", "data": serializer.data})
        return Response({"error": serializer.errors})
    

class CustomerDetail(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_object(self, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            self.check_object_permissions(self.request, customer)
            return customer
        except:
            raise Http404
        
    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        customer = self.get_object(pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Update Successfull", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk=pk)
        customer.delete()
        return Response({"message": "Delete Successfull"}, status=status.HTTP_200_OK)
    

class CustomerOrderList(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_customer(self, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            self.check_object_permissions(self.request, customer)
            return customer
        except Customer.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        customer = self.get_customer(pk=pk)
        orders = Order.objects.filter(ordered_by=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)