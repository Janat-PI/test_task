from rest_framework import serializers

from .models import (
    Client, Service,
    OrderItem, Organization, Card
)
from .schemas import Data


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        models = Client
        fields = ("name", )


class OrgranizationSerializer(serializers.ModelSerializer):

    class Meta:
        models = Client
        fields = ("name", )


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        models = Service
        fields = ("title", "price")


def parsing_data(data) -> list[Data]:
    import pandas as pd
    from datetime import date as built_in_date

    results_data = []

    data_ = pd.read_csv(data)
    data_columns = pd.DataFrame(data_, columns=['client_name', 'client_org', '№', 'sum', 'date', 'service'])
    for i in data_columns.iterrows():
        client = i[1].client_name
        org = i[1].client_org
        number = i[1]['№']
        sum_ = i[1]['sum']
        date = i[1].date
        index = i[0]
        try:
            day, month, year = map(int, date.split("."))
        except:
            raise ValueError(f"Jopa in date in line {index} in data")
        else:
            date = built_in_date(year=year, month=month, day=day)
        
        try:
            sum_ = int(sum_)
        except:
            raise ValueError(f"sum not valid jopa line {index} in data")
            
        service = i[1].service

        schema_data = Data(
            client_name=client,
            org=org,
            sum_=sum_,
            date=date,
            service=service
        )

        results_data.append(schema_data)
    
    return results_data
        


class BillSerializer(serializers.Serializer):

    data = serializers.FileField()

    def validate(self, attrs):
        data = attrs["data"]

        try:
            results = parsing_data(data)
        except Exception as e:
            raise serializers.ValidationError(e)

        service_data = []
        order_item_data = []
        
        for data_ in results:
            client, _ = Client.objects.get_or_create(name=data_.client_name)
            organization, _ = Organization.objects.get_or_create(name=data_.org)
            service = Service(
                title=data_.service,
                total_sum=data_.sum_
            )
      
            order_item = OrderItem(
                org_name=organization,
                service=service,
                card_id=client.card,
                create_date=data_.date
            )

            service_data.append(service)
            order_item_data.append(order_item)
        
        Service.objects.bulk_create(service_data)
        OrderItem.objects.bulk_create(order_item_data)

            
        return super().validate(attrs)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1


class BillInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["all_data"] = OrderItemSerializer(instance.card.order_items.all(), many=True).data
        return rep








