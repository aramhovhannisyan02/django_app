from django.shortcuts import render, get_object_or_404
from .models import (
    ItemsModel,
    TableItem,
    UserTable,
    BigTable,
    Debt
)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from django.shortcuts import redirect

from account.forms import PaymantForm

# Create your views here.


def home(request):
    User = request.user
    Items = ItemsModel.objects.all()

    return render(request, 'tables/home.html', {'Items': Items, 'user': User})


@login_required
@csrf_exempt
def save_table_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)['data']
        # print(data)
        table_name = json.loads(request.body)['table_name']
        table = UserTable.objects.create(
            user=request.user,
            tableName=table_name
        )

        debt_sum = json.loads(request.body)['total-sum']

        debt = Debt.objects.create(
            customer = request.user,
            debt = int(debt_sum)
        )
        debt.save()
        
        # bigtable = get_object_or_404(BigTable, request.user.id)
        # print(bigtable,'bigtablle')
        for item in data:
            # print(item)
            table_item = TableItem.objects.create(
                table=table,
                product_name=item['productName'],
                product_count=item['productCount'],
                product_price=item['productPrice'],
                total_price=item['totalPrice']
            )
            table_item.save()

        try:
            bigtable = BigTable.objects.get(user=request.user)
        except BigTable.DoesNotExist:
            bigtable = False
        if bigtable:
            bigtable.table = table
            bigtable.save()
        else:
            bigtable = BigTable.objects.create(user=request.user, table=table)
            # bigtable.save()
        return JsonResponse({'message': 'Table data saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def Paymant(request):
    if request.method == 'POST':
        form = PaymantForm(request.POST)
        if form.is_valid():
            debt = Debt.objects.create(customer=request.user, debt=-float(request.POST.get('debt')))
            debt.save()
            return redirect('customer')
        return redirect('customer')
    return redirect('customer')