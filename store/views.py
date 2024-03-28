from django.shortcuts import render 
from django.http import JsonResponse
import json
from .models import *

# Create your views here.


def store(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = [] 
        order={"get_cart_total" : 0 , "get_cart_items" : 0} 
        cartItems = order["get_cart_items"]
   
    products = Product.objects.all()
    context={"products": products , 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items=[] 
        order={"get_cart_total" : 0 , "get_cart_items" : 0}
        cartItems = order["get_cart_items"]   
    context={"items":items , "order":order ,'cartItems':cartItems }
    return render(request , 'store/checkout.html' , context)


def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items=[] 
        order={"get_cart_total" : 0 , "get_cart_items" : 0}
        cartItems = order["get_cart_items"]   
    context={"items":items , "order":order , 'cartItems':cartItems}
    return render(request , 'store/cart.html' , context)

#def parviz(request):
    #products = Product.objects.all()
    #return HttpResponse(products)

def updateitem(request):
    data = json.loads(request.body)
    productID = data["productId"]
    action = data["action"]
    print('Action: ' , action)
    print('productID: ' , productID)
    
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer , complete=False)
    orderItem , created = orderitem.objects.get_or_create(order=order , product=product)
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()      
    
    if orderItem.quantity <= 0:
        orderItem.delete()
            
    orderItem.save()        
    return JsonResponse('item was adeed' , safe=False)
    