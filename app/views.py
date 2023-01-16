from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        laptops=Product.objects.filter(category='L')
        mobiles=Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'laptops':laptops, 'mobiles':mobiles} )



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product =Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})




def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product_id).save()
    return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active': 'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data == 'Redmi' or data=='Apple' or data=='Samsung':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data == 'Above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=50000)
    elif data == 'Below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=50000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data == 'Dell' or data=='HP' or data=='Apple':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data == 'Above':
        laptops=Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    elif data == 'Below':
        laptops=Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    return render(request, 'app/laptop.html', {'laptops':laptops})



def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form =CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form =CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})



def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save();
            messages.success(request, 'Congratulations!! Profile Updated successfully')
            return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})