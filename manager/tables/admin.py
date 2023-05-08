from django.contrib import admin
from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt
)
# Register your models here.
admin.site.register(ItemsModel)
admin.site.register(TableItem)
admin.site.register(UserTable)
admin.site.register(BigTable)
admin.site.register(Debt)

