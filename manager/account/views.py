from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, ItemAddForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.decorators import login_required
from tables.models import (
    ItemsModel,
    UserTable,
    TableItem,
    BigTable,
    Debt
)
from account.models import (
    User
)

from django.core.paginator import Paginator

from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def admin(request):
    users = User.objects.filter(is_customer = True)

    if request.method == 'POST':
        # print(request.POST['customer'])
        form = ItemAddForm(request.POST)
        if form.is_valid():
            # print('Aram')
            form.save(commit=False)
            form.save()
            return redirect('adminpage')
    else:
        # print('Erooooooooooooooooor')
        form = ItemAddForm()

    items = ItemsModel.objects.all()
    return render(request, 'admin.html', {'Items': items, 'Users': users, })


@login_required
def customer(request):
    tablesUsers = UserTable.objects.all()
    items = ItemsModel.objects.all()
    tableRows = TableItem.objects.all()
    print(tableRows)
    return render(request, 'customer.html', {'Items': items, 'Tables': tablesUsers, 'TableRows': tableRows})


@login_required
def employee(request):

    tablesUsers = UserTable.objects.all()
    items = ItemsModel.objects.all()
    tableRows = TableItem.objects.all()
    bigTables = BigTable.objects.all()
    # debt = 
    return render(request, 'employee.html', {
        'Items': items,
        'Tables': tablesUsers,
        'TableRows': tableRows,
        'BigTable': bigTables
    })


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('adminpage')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_item_all(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    # return redirect('productsforall')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_item_byuser(request, item_id):
    item = get_object_or_404(ItemsModel, id=item_id)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edit_item(request, item_id):
    customers = User.objects.filter(is_customer=True)
    item = get_object_or_404(ItemsModel, id=item_id)
    if request.method == 'POST':
        form = ItemAddForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('adminpage')
            # return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ItemAddForm(instance=item)
    return render(request, 'edit_item.html', {'form': form,'item':item, 'Users': customers})

@login_required
def allCustomers(request):
    allCustomers = User.objects.filter(is_customer = True)
    return render(request, 'allcustomers.html',{'allCustomers':allCustomers})

# @login_required
# def customerTables(request, user_id):
#     customer = User.objects.filter(id = user_id)
#     tablesUsers = UserTable.objects.filter(user_id = user_id)
#     tableRows = TableItem.objects.all()
#     return render(request, 'customerTables.html', {'tables':tablesUsers, 'Rows':tableRows, 'customer':customer})


@login_required
def customerTables(request, user_id):
    customer = User.objects.get(id = user_id)
    tablesUsers = UserTable.objects.filter(user_id = user_id)
    tableRows = TableItem.objects.all()
    
    paginator = Paginator(tablesUsers, 5) # show 10 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'customerTables.html', {'tables':page_obj, 'Rows':tableRows, 'customer':customer})


@login_required
def tablesByUser(request):
    tablesbyUser = UserTable.objects.filter(user = request.user)
    tableRows = TableItem.objects.all()
    
    paginator = Paginator(tablesbyUser, 5) # show 10 tables per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    debt = Debt.objects.filter(customer = request.user)


    return render(request, 'tablesbyUser.html', {'tables':page_obj, 'Rows':tableRows, 'debt_row': debt})

@login_required
def allCustomersforAdmin(request):
    allCustomers = User.objects.filter(is_customer = True)
    return render(request, 'allcustomersforAdmin.html',{'allCustomers':allCustomers})

@login_required
def customersProducts(request, user_id):
    customer = User.objects.get(id = user_id)
    Products = ItemsModel.objects.all()
    return render(request, 'customerProducts.html', {'customer': customer, 'products':Products})

@login_required
def productsForAll(request):
    Products = ItemsModel.objects.filter(customer = 'all')
    return render(request, 'productsforAll.html', {'products': Products})

def customerDebt(request, user_id):
    customer = User.objects.get(id = user_id)

    customersDept = Debt.objects.filter(customer_id = user_id)

    return render(request, 'customersDebt.html', {
        'customer':customer,
        'debt_row': customersDept,
    } )
