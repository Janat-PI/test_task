from django.db import models

class AbstracClassModel(models.Model):
    
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True


class Client(AbstracClassModel):
    pass


class Organization(AbstracClassModel):
    pass


class Service(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)


class Card(models.Model):
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True, related_name="card")
    

class OrderItem(models.Model):
    org_name = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="order_items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="order_items")
    card_id = models.ForeignKey(Card, on_delete=models.PROTECT, related_name="order_items")
    create_date = models.DateField()