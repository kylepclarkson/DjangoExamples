from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Customer, Product, Order
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


def registerPage(request):

    if request.user.is_authenticated:
        # redirect authenticated users to home page
        return redirect('home')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def loginPage(request):

    if request.user.is_authenticated:
        # redirect authenticated users to home page
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login in user
            login(request, user)
            return redirect('home')
        else:
            # login error
            messages.info(request, 'Username or password is incorrect.')
            return redirect('login')
    context = {}

    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)



@login_required(login_url='login')
def customer(request, pk):

    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    # use filter to display orders
    myFilter = OrderFilter(request.GET,
                           queryset=orders)
    # apply filter
    orders = myFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    # Create inline order set using parent/child tables
    OrderFormSet = inlineformset_factory(Customer,
                                         Order,
                                         fields=('product', 'status',),
                                         extra=4)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(
        queryset=Order.objects.none(), #dont display objects in form
        instance=customer)
    # form = OrderForm(initial=
    #     {'customer': customer}
    # )
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        # 'form': form,
        'formset': formset
    }


    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):

    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }

    return render(request, 'accounts/delete.html', context)

