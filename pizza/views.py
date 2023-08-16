from django.shortcuts import render
from django.http import Http404
from .models import Pizza, Order, Customer
from .serializers import PizzaSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Import the permission
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin

# Create your views here.
class PizzaList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Require authentication
    
    def get(self, request):
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PizzaDetail(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_object(self, pk):
        try:
            return Pizza.objects.get(pk=pk)
        except Pizza.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        pizza = self.get_object(pk=pk)
        serializer = PizzaSerializer(pizza)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        pizza = self.get_object(pk=pk)
        serializer = PizzaSerializer(pizza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pizza = self.get_object(pk=pk)
        pizza.delete()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


class OrderList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Require authentication

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # breakpoint()
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):

    def get_object(self, pk):
        try:
            # breakpoint()
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(self.request, order)
            return order
        except Order.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        order = self.get_object(pk=pk)
        # breakpoint()
        serializer = OrderSerializer(order)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        order = self.get_object(pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        order = self.get_object(pk=pk)
        order.delete()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


# class OrderPizzas(APIView):
#     def get_pizzas(self, request, pk):
#         try:
#             order = Order.objects.get(pk=pk)
#             serializer = OrderSerializer(order)
#             return Response(serializer.data.pizzas)
#         except:
#             raise Http404

