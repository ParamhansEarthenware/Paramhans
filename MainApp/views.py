from django.shortcuts import render,HttpResponseRedirect
from . import forms
from django.contrib.messages import success,error
from django.db.models import Q
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.mail import send_mail

from MainApp.models import *
from PARAMHANS import settings
def Home(request):
    if (request.method == 'POST'):
        data = Product.objects.all()
    else:
        data = Product.objects.all()
    return render(request, "index.html", {"Data": data})

def Login(request):
    if(request.method=='POST'):
        lname=request.POST.get('usernam')
        lpward=request.POST.get('passwrd')
        user=auth.authenticate(username=lname,password=lpward)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect('/')
        else:
            error(request,"Invalid User")
    return render(request,'Login.html')

def Signup(request):
    if(request.method=='POST'):
        uname=request.POST.get('uname')
        try:
            match = User.objects.get(username=str(uname))
            if (match):
                error(request, "Username Already Exist")

        except:
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            mailid = request.POST.get('email')
            pward = request.POST.get('pward')
            cpward = request.POST.get('cpward')
            if (pward == cpward):
                User.objects.create_user(username=str(uname),
                                         first_name=str(fname),
                                         last_name=str(lname),
                                         email=mailid,
                                         password=pward
                                         )
                success(request, "Account is created")
                Signup_email(request, mailid, fname,uname)
                return HttpResponseRedirect('/Login/')
            else:
                error(request, "Password and Confirm Password not Matched")
    return render(request, "signup.html")


def Shop(request,cn):
    if (cn == "sample"):
        data = Product.objects.all()
    else:
        data = Product.objects.all()


    return render(request,"shop.html",{"Data":data})

def ProductDetails(request,num):

    data = Product.objects.get(id=num)
    if (request.method == 'POST'):
        form = forms.CartForm(request.POST)
        print(form)
        q = request.POST['count']
        print(form.is_valid())
        if (form.is_valid()):
            f = form.save(commit=False)
            f.cart_user = request.user
            f.cart_product = data
            f.count = q
            f.total = int(data.price) * float(q)
            f.save()
            return HttpResponseRedirect('/cart/')
    else:
        form = forms.CartForm()
    return render(request, 'product-details.html', {"Data": data, "Form": form})


def Logout(request):
    if (request.method == 'POST'):
        data = Product.objects.all()
    else:
        data = Product.objects.all()
    auth.logout(request)
    return render(request,"index.html", {'Data': data})


def Admin(request):
    data=Product.objects.all()
    return render(request,"Admin.html",{"Data":data})


def AddProduct(request):
    if (request.method == 'POST'):
        try:
            data = Product()
            data.pid = request.POST.get('id')
            data.id = request.POST.get('id')
            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            bp = int(data.basicPrice)
            d = int(data.discount)
            data.price = int(bp - (bp * d / 100))
            data.img1 = request.FILES.get('img1')
            data.img2 = request.FILES.get('img2')
            data.img3 = request.FILES.get('img3')
            data.img4 = request.FILES.get('img4')
            data.save()
            success(request, 'Product Inserted')
            return HttpResponseRedirect('/AddProduct/')
        except:
            error(request, "Invalid Record")
    return render(request, "AddProduct.html" , {'Form' : forms.ProductForm})


def EditProduct(request,num):
    data=Product.objects.get(id=num)
    if (request.method == 'POST'):
        try:
            data.name = request.POST.get('name')
            data.description = request.POST.get('description')
            data.basicPrice = request.POST.get('basicPrice')
            data.discount = request.POST.get('discount')
            bp = int(data.basicPrice)
            d = int(data.discount)
            data.price = bp - bp * d / 100
            data.color = request.POST.get('color')
            data.save()
            success(request, 'Product Edited')
            data = Product.objects.get(id=num)
        except:
            error(request, "Invalid Record")
    return render(request,"edit.html",{"Data":data})



def DeleteProduct(request,num):
    data=Product.objects.get(id=num)
    data.delete()
    data = Product.objects.all()
    return render(request,"Admin.html",{"Data":data})


def Signup_email(request,email,name,uname):
    subject = 'Thanks '+name+' for registering to our website.'
    message = ' We are glad to serve you.'+"\n\n"+'About Us'+"PARAMHANS EARTHENWARE AROMA SALES"+"\n\n"+"Offering you the best of kitchen household products- designed pottery,which serves the purpose of both art and healthy,non-toxic food."+"\n\n"+"Delivering utensils to your doorstep that are eco-friendly,easy to clean and preserve the nutritional values of food."+"\n\n"+"OUR SOIL IS GOLD,EAT IN GOLD"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail( subject, message, email_from, recipient_list )


def order_delivered(request,data):
    subject = 'Order delivered'
    message = 'Dear '+data.order_address.chname+',\n Your Product has been delivered .\nAt address: \n'+data.order_address.address+"\n"+data.order_address.pin
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.order_address.email,]
    send_mail( subject, message, email_from, recipient_list )

@login_required(login_url='/Login/')
def CartDetails(request):
    data=Cart.objects.filter(cart_user=request.user)
    total=0
    for i in data:
        totalt=total+i.cart_product.price*i.count
    return render(request,"cart.html",{"Data":data,"Total":total})


@login_required(login_url='/Login/')
def LastOrders(request):
    data=Order.objects.filter(order_user=request.user)
    return render(request,"oldorders.html",{"Data":data})


@login_required(login_url='/Login/')
def Ordered(request):
    data=DeliveredOrder.objects.filter(order_user=request.user)
    return render(request,"oldorders.html",{"Data":data})



def CartDelete(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.delete()
    data=Cart.objects.filter(cart_user=request.user)
    total = 0
    for i in data:
        total = total + i.cart_product.price * i.count
    return render(request, "cart.html", {"Data": data,"Total":total})


def minus(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)-1
    if(int(data.count)==0):
        data.count=1
    data.save()
    print(data.count)
    data = Cart.objects.filter(cart_user=request.user)
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count
    return render(request, "cart.html", {"Data": data, "Total": t})



def OrderPlaced(request):
    data=DeliveredOrder.objects.filter(order_user=request.user)
    return render(request,"orderplaced.html",{"Data":data})


def plus(request,num):
    data=Cart.objects.get(cart_product__id=num)
    data.count= int(data.count)+1
    data.save()
    data = Cart.objects.filter(cart_user=request.user)
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count
    return render(request, "cart.html", {"Data": data, "Total": t})


def Address(request):
    Na=""
    if (request.method == 'POST'):
         try:
            check = Checkout()
            check.checkid= request.user
            Na=request.user
            check.chname = request.POST.get('name')
            check.checkout_user = request.user
            check.mobile = request.POST.get('mobile')
            check.email = request.POST.get('email')
            check.state = request.POST.get('state')
            check.city = request.POST.get('city')
            check.address = request.POST.get('address')
            check.pin = request.POST.get('pin')
            check.save()
            success(request, "Address is added")
            y = "/checkout/" + str(Na) + "/"
            return HttpResponseRedirect(y)
         except:
            error(request, "Invalid Record")
    return render(request, "Address.html")

MERCHANT_KEY='sample'
@login_required(login_url='/Login/')
def CheckoutForm(request,num):
    data = Cart.objects.filter(cart_user=request.user)
    t = 0
    for i in data:
        t = t + i.cart_product.price * i.count
    Cdata=Checkout.objects.filter(checkid=num)
    Odata=Order.objects.all()
    if(Odata != None):
        for N in Odata:
            t=int(N.ordernumber)
    if(request.method=='POST'):
        choice = request.POST.get('choice')
        if(choice=='COD'):
            for i in data:
                Or = Order()
                Or.ordernumber = t+1
                t=t+1
                Or.order_user = request.user
                Pro = Product.objects.get(id=i.cart_product.id)
                Or.order_product = Pro
                for ADD in Cdata:
                    Or.order_address = ADD
                Or.count = i.count
                Or.save()
            data.delete()
            success(request,"Order Placed")
            return HttpResponseRedirect('/orderplaced/')
        elif\
                (choice=='Paytm'):
            success(request, "PAYTM")
            return HttpResponseRedirect('/payment/process/')
    ''' elif (choice == 'PAYTM'):
            # request paytm to transfer the amount to your account after paytm by user
            param_dict = {
                'MID': 'WorldP64425807474247',
                'TXN_AMOUNT': str(t),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = checksum.generate_checksum, param_dict,
            return render(request, 'paytm.html', {'param_dict': param_dict})'''

    return render(request,"checkout.html",{"Total":t,"Data":Cdata})



def AdminCorner(request):
    data=Order.objects.all()
    return render(request,'AdminCorner.html',{"Data":data})


def OrderDelivered(request,num):
    data = Order.objects.get(ordernumber=num)
    D = DeliveredOrder()
    D.ordernumber = data.ordernumber
    D.order_user = data.order_user
    D.order_product = data.order_product
    D.count=data.count
    D.order_address = data.order_address
    print(D.count)
    D.save()
    order_delivered(request,data)
    data.delete()
    data=Order.objects.all()
    return render(request,'AdminCorner.html',{"Data":data})

