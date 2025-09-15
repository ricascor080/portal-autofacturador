from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)

    # Para que cree automáticamente el schema en la DB
    auto_create_schema = True


class Domain(DomainMixin):
    pass
