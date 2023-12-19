from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

from .models import *
from django.contrib.auth.hashers import make_password,check_password

def index(request):
    if request.method == "POST":
        product_id= request.POST.get('cartid')
        product_id= request.POST.get('minus')
        
        card_id= request.session.get('cart')
        
        
        if cart_id:
            quantity=cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <=1:
                        cart_id.pop(product_id)
                    else:
                         cart_id[product_id]=quantity - 1
                        
                cart_id[product_id]=quantity + 1
            else:
                cart_id[product_id]=1
        else:
            cart_id={}
            cart_id[product_id]=1
            
            request.session['cart']=cart_id
            
            
            
           
            
        
        
        
    category_obj= Category.objects.all()
    category_id=request.GET.get('cate_id')
    search=request.GET.get('search')
    
    
    if category_id:
        product_obj= Product.objects.filter(category=category_id)
        
    elif search:
        product_obj= Product.objects.filter(product_name__icontains=search)
        
    else:
        product_obj= Product.objects.all()
    
    context={
        'category': category_obj,
        'product': product_obj,
    }
    return render(request, 'home.html',context=context)


def signup(request):
    if request.method =='POST':
        f_name=request.POST.get('fname')
        l_name=request.POST.get('lname')
        email=request.POST.get('emailid')
        password=request.POST.get('pwd')
        mobile=request.POST.get('mbl')
        gender=request.POST.get('gender')
        
        
        reg_obj= Registrations(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender
        )
        
        reg_obj.save()
        
        
        return redirect('home')
    
    
    
def login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('pwd')
        
        try:
            login_obj=Registrations.objects.get(email=email)
            if check_password(password, login_obj.password):
                request.session['name'] = login_obj.first_name
                request.session['customer'] = login_obj.id
                return redirect('home')
            else:
                return HttpResponse("Invalid Password")
            
        except:
            return HttpResponse("Email not found")
        
def logout(request):
    request.session.clear()
    return redirect('home')


def cart_details(request):
    cart_keys=list(request.session.get('cart').keys())
    product=Product.objects.filter(id__in=cart_keys)
    context={
        'product': product
        
    }
    return render(request,'cart.html', context=context)


def checkout(request):
    if request.method == 'POST':
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        
        customer_id=request.POST.get('customer_id')
        if not customer_id:
            return redirect('home')
            #return HttpResponse("Please login to checkout")
        cart_keys=request.session.get('cart').keys()
        product=Product.objects.filter(id__in=list(cart_keys.keys()))

        for p in product:
            order_obj=Order(
                address=address,
                mobile=mobile,
                customer=Registrations(id=customer_id),
                product=p,
                price=p.product_price,
                quantity=cart_keys.get(str(p.id)),
                status=False
            )
            order_obj.save()
        return render(request, 'order.html')

def order(request):
    customer_id=request.session.get('customer')
    order_obj=Order.objects.filter(customer=customer_id)
    tp=0
    for i in order_obj:
        tp=tp+ (i.price*i.quantity)
        
    request.session['cart']= {}
        
    
    
    return render(request, 'order.html',{'order': order_obj,'tp':tp})

from rest_framework import routers, serializers, viewsets
from .serializers import *
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registrations.objects.all()
    serializer_class = RegistrationSerializer
            
        

    
                
        