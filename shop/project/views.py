from django.shortcuts import redirect, render
from .models import  Address, Product,Cart,City
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,logout as django_logout, login as auth_login
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseNotFound
from .forms import AddressForm, Signupform,MyUserChangeForm
import datetime
from .models import Order
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
stripe.api_key="sk_test_51L2TV5SBnyV9WLBjK9AF2s5bwq0oVhsgdxzIWFpkO1CYbkZqn8ID3JEfWFWyFhbf2ilKqQbpfroEincm8loi31gD00tu2wvisi"
# Create your views here.
@csrf_exempt
def add_address(request):
    if request.method=="POST":
        current_user=request.user
        form=AddressForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address= form.cleaned_data['address']
            pincode = form.cleaned_data['pincode']
            mobile_no= form.cleaned_data['mobile_no']
            country= form.cleaned_data['country']
            city = form.cleaned_data['city']
            c=Address(first_name=first_name,user_id=current_user.id,last_name=last_name,address=address,mobile_no=mobile_no,country=country,city=city,pincode=pincode)
            c.save()
            messages.success(request,'Account created successfully')  
            return redirect('updateProfile')
    else:
        form=AddressForm()
    return render(request,'project/address_form.html',{'form':form})
        


def load_cities(request):   
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'project/city.html', {'cities': cities})

def index(request):
    pro=Product.objects.all()
    return render(request,"index.html",{'pro':pro})
@csrf_exempt
def createuser(request):
    if request.method=="POST":
        form=Signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully')  
            return redirect("login")
    else:
        form=Signupform()
    return render(request,"createuser.html",{'form':form})
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = auth_login(request,user)
            return redirect("index")
        else:
            messages.info(request,'invalid username or password')     
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def logout(request):
   django_logout(request)
   return redirect("login") 

#cart
def cart(request):
    if request.user.is_authenticated:
        current_user=request.user
        product_id=request.GET["product_id"]
        item=Cart.objects.filter(product_id=product_id,userid=current_user.id).exists()
        if item!=True:
            obj=Product.objects.filter(id=product_id).values()
            add=Cart(product_id=product_id,price=obj[0]['price'],userid=current_user.id,quantity=1)
            add.save()
            response = {'status': 'success'}
            return JsonResponse(response)
        else:        
           response = {'status': 'failed'}
           return JsonResponse(response)
    else:
        return redirect("login")
         
def cartdata(request):
    if request.user.is_authenticated:
        current_user=request.user
        obj=Cart.objects.select_related('product').filter(userid=current_user.id)
        if len(obj)>0:  
            total = 0
            for a in obj:
                 total = total + (a.quantity * a.price)
            return render(request,"cartdata.html",{'obj':obj,'total':total})
        else:
            return render(request,"empty.html")
    else:
        return redirect("login")

def deletecart(request):
    removecart=request.GET["remove_cart"]

    obj=Cart.objects.filter(id=removecart)
    obj.delete()
    response = {'status': 'success', 'message': 'product has been deleted'}
    return JsonResponse(response)
@csrf_exempt
def passwordchange(request):
    if request.method=="POST":
        user=request.user
        data=request.POST
        obj=PasswordChangeForm(user,data)
        if obj.is_valid():
            obj.save()
            update_session_auth_hash(request,obj.user)
            messages.info(request,'Password Change Successfully')   
    else:
        obj=PasswordChangeForm(user=request.user)
    return render(request,"passwordchange.html",{'password':obj})

def checkout(request):
    current_user = request.user
    show=Address.objects.filter(user_id=current_user.id)
    list =Cart.objects.select_related('product').filter(userid = current_user.id)
    total = 0
    for obj in list:
     total = total + (obj.quantity * obj.price)
    return render(request,"checkout.html",{'checkList':list,'grandtotal':total,'showAddress':show})


def checkoutSession(request):
    current_user = request.user
    addressId=request.GET.get("addressId")
    list =Cart.objects.select_related('product').filter(userid = current_user.id)
    obj = list[0]   
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(            
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(obj.price * 100),
                        'product_data': {
                            'name': obj.product.name,
                        },
                    },
                    'quantity': obj.quantity,
                },
            ],
            metadata={
                "product_id": obj.product_id
            },
            mode='payment',
            customer_email = current_user.email,
            success_url=YOUR_DOMAIN +'/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel',
    )
    order = Order()
    order.product_id = obj.product_id
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.email=checkout_session['customer_email']
    order.price = int(checkout_session['amount_total']/100)
    order.quantity = obj.quantity
    order.userid = current_user.id
    order.status = 'Cancel'
    order.created_at = datetime.date.today()
    order.address_id = addressId
    order.save()
    return JsonResponse({
            'id': checkout_session.id
        })

def success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
       return HttpResponseNotFound()
    else:
        session = stripe.checkout.Session.retrieve(session_id)
        current_user = request.user
        list=User.objects.filter(id=current_user.id).values()
        obj= Order.objects.filter(stripe_payment_intent=session.payment_intent).update(status="success", has_paid=True)
        orders=Order.objects.filter(userid=current_user.id)
        current_user = request.user
        Cart.objects.filter(userid=current_user.id).delete()
        # send_mail(
        #     subject="Shoppers",
        #     message="your order has been confirmed",
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[current_user.email],
        #     fail_silently=False
        # )
        return render(request,"success.html",{'orders':orders[0],'list':list})

def order(request):
    if request.user.is_authenticated:
        current_user = request.user
        dataset= Order.objects.filter(userid=current_user.id).order_by('-created_at')
        return render(request, "order.html",{'dataset':dataset})
    else:
        return redirect("login")
@csrf_exempt
def updateProfile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            obj=MyUserChangeForm(request.POST,instance=request.user)
            current_user=request.user
            email=request.POST['email']
            if User.objects.filter(email=email).exclude(id=current_user.id).exists():
                messages.info(request,"Email Already exists")
            elif obj.is_valid():
              obj.save()
              messages.success(request,"Account Updated Successfully")
              return redirect("updateProfile")
        else:
            obj=MyUserChangeForm(instance=request.user)
            current_user=request.user
        dataset= Address.objects.filter(user_id=current_user.id)
        return render(request,"account.html",{'obj':obj,'dataset':dataset})
    else:
        return redirect("login")
@csrf_exempt
def updateAddress(request,id):
    if request.method=="POST":
        obj=Address.objects.get(id=id)
        form=AddressForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Address Updated Successfully')
            return redirect("updateProfile")
    else:
        obj=Address.objects.get(id=id)
        form=AddressForm(instance=obj)
    return render(request,"project/update.html",{'form':form})

def delete_address(request,id):
    obj=Address.objects.filter(id=id)
    obj.delete()
    messages.success(request, f'Record Deleted Successfully')
    return redirect("updateProfile")



# def updateProfile(request):
#     form = MyUserChangeForm(request.POST, instance=request.user)
#     username = request.POST['username']
#     current_user = request.user
#     email=request.POST["email"]
#     data = {
#         'is_taken': User.objects.filter(username__iexact=username).exclude(id= current_user.id).exists(),
#         'is_email_taken':User.objects.filter(email=email).exclude(id= current_user.id).exists()
#     } 
    
#     if request.user.is_authenticated and request.method == 'POST' and form.is_valid() and data['is_taken'] == False and data['is_email_taken'] == False:

#         form.save()
#         response = {'status': 'success'}
#         return JsonResponse(response)
#     else:    

#         response = {'status': 'failed','error_data': data}
#         return JsonResponse(response)



def delete_user(request):
    current_user=request.user
    obj=User.objects.filter(id=current_user.id)
    obj.delete()
    obj=Order.objects.filter(id=current_user.id).delete()
    obj=Cart.objects.filter(id=current_user.id).delete()
    messages.info(request,'Account has been deleted')
    return redirect("login")
    
def account(request):
    if request.user.is_authenticated:
        current_user = request.user
        updateProfileform=MyUserChangeForm(instance=request.user)
        return render(request, 'account.html',{'updateData': updateProfileform})      
    else:
        return redirect("login")
@csrf_exempt
def updateQuantity(request):
    cart_id=request.POST['cart_id']
    quantity=request.POST['quantity']
    print(quantity)
    cart=Cart.objects.filter(id=cart_id).update(quantity= int(quantity))
    return JsonResponse({})
