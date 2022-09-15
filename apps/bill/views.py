from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


from .serializers import BillSerializer, BillInfoSerializer, OrderItemSerializer
from .models import Client, Organization


class BillView(APIView):

    def post(self, request):
        data = request.data

        serializer = BillSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            return Response(data=serializer.validated_data)

        return Response("data")
        


class BillInfo(ListAPIView):

    queryset = Client.objects.all()
    serializer_class = BillInfoSerializer


class ClientInfo(APIView):

    def get(self, request, client: str, org: str):

        client = get_object_or_404(Client, name=client)
        org = get_object_or_404(Organization, name=org)
        data = client.card.order_items.all().filter(org_name=org)

        serializer = OrderItemSerializer(data, many=True)
        
        return Response(serializer.data)
