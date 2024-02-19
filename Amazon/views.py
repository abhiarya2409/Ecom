from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

from .models import *
from django.contrib.auth.hashers import make_password,check_password

def index(request): 
    if request.method == "POST":
        
        product_id = request.POST.get("cartid")
        remove = request.POST.get("minus")

        print("product_id------------------: ", product_id)

        cart_id = request.session.get('cart')
        print("cart_id------------------: ", cart_id)
        # print(cart_id)
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                         cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
        request.session['cart'] = cart_id 
        # print(request.session['cart'])

    category_obj = Category.objects.all()
    category_id = request.GET.get('cate_id')
    search = request.GET.get('search')
    best_of_fashion  = None
    Best_of_fitness= None
    fashion_category = Category.objects.get(category_name='Fashion')
    fitness_category = Category.objects.get(category_name='Fitness')
      
    best_of_fashion = Product.objects.filter(category=fashion_category)
    best_of_fitness = Product.objects.filter(category=fitness_category)
    # fitness_category = Category.objects.get(category_name='Fitness')
    # best_of_fitness = Product.objects.filter(category=fitness_category)

    if category_id and fashion_category:
        product_obj = Product.objects.filter(category=category_id)
    elif search:
        product_obj = Product.objects.filter(product_name__icontains=search)
        
    if category_id and fitness_category:
        product_obj = Product.objects.filter(category=category_id)
    elif search:
        product_obj = Product.objects.filter(product_name__icontains=search)
        
    # elif fashion_category:
    #    best_of_fashion = Product.objects.filter(category=fashion_category)
    #    print(best_of_fashion)
    # elif fitness_category:
    #    best_of_fitness = Product.objects.filter(category=fitness_category)
    else:    
        product_obj = Product.objects.all()

    context = {
        'category': category_obj,
        'product': product_obj,
        'best_of_fashion': best_of_fashion,
        'best_of_fitness': best_of_fitness,
        'category_id':category_id
    }
    return render(request, 'home.html', context=context)



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
    







            
        

    
                
        