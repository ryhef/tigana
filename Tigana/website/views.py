from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from store.models import Item, ItemImage, Inquiry
from store.forms import InquiryForm
from orders.models import Order, LineItem


from orders.cart import Cart
from orders.forms import CartAddProductForm


#
#
class home(View):
    def get(self,request):
        return render(request,'website/home.html')

#
#
class shop(View):
    def get(self, request):
        items = Item.objects.order_by('pk')
        images = ItemImage.objects.order_by('pk')
        context = {'images':images,'items':items}
        return render(request, 'website/shop.html',context)

#
#
class shop_detail(View):
    def get(self, request, id):
        itemDetail = get_object_or_404(Item, pk=id)
        itemImages = get_list_or_404(ItemImage, item__pk=id)
        cart_product_form = CartAddProductForm()
        error_flag = 0
        return render(request, 'website/shopdetail.html', {'item':itemDetail, 'itemImages':itemImages, 'cart_product_form': cart_product_form,'error_flag':error_flag} )


    def post(self, request, id):
        itemDetail = get_object_or_404(Item, pk=id)
        itemImages = get_list_or_404(ItemImage, item__pk=id)
        cart_product_form = CartAddProductForm()
        error_flag = 0

        cart = Cart(request)
        product = get_object_or_404(Item, id=id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if product.item_qty < int(cd['quantity']):
                error_flag = 1
                return render(request,'website/shopdetail.html',{'item':itemDetail, 'itemImages':itemImages, 'cart_product_form': cart_product_form,'error_flag':error_flag})
            cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
        return redirect('website:cart')


#
#
class inquiry_received(View):
    def post(self, request):
        form = InquiryForm(request.POST)
        if form.is_valid():
            customer_first_name = form.cleaned_data['customer_first_name']
            customer_last_name = form.cleaned_data['customer_last_name']
            customer_email = form.cleaned_data['customer_email']
            customer_phone = form.cleaned_data['customer_phone']
            contact = form.cleaned_data['prefered_contact_method']
        newInquiry = Inquiry(customer_first_name=customer_first_name, customer_last_name=customer_last_name, customer_email=customer_email,customer_phone=customer_phone, status='Received', prefered_contact_method=contact,question=request.POST['question'])
        #newInquiry = Inquiry(customer_first_name=request.POST['firstname'], customer_last_name=request.POST['lastname'], customer_email=request.POST['email'],customer_phone=request.POST['phone'], status='Received', prefered_contact_method=request.POST['contact'],question=request.POST['question'])
        newInquiry.save()
        #newInquiry.inquiry_received_email()
        return render(request,'website/received.html')

#
#
class contact(View):
    def get(self, request):
        form = InquiryForm()
        return render(request,'website/contact.html',{'form':form})


class cart(View):
    def get(self, request):
        cart = Cart(request)
        cart_product_form = CartAddProductForm()
        total_price = cart.get_total_price()
        error_flag = 0
        return render(request,'website/cart.html', {'cart':cart, 'cart_product_form': cart_product_form,'totalPrice':total_price,'error_flag':error_flag})


    def post(self, request, id):
        if request.POST['status'] == 'Remove':
            cart = Cart(request)
            product = get_object_or_404(Item, id=id)
            cart.remove(product)
            return redirect('website:cart')
        else:
            cart = Cart(request)
            product = get_object_or_404(Item, id=id)
            form = CartAddProductForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if product.item_qty < int(cd['quantity']):
                    error_flag = 1
                    cart_product_form = CartAddProductForm()
                    total_price = cart.get_total_price()
                    return render(request,'website/cart.html', {'cart':cart, 'cart_product_form': cart_product_form,'totalPrice':total_price,'error_flag':error_flag, 'product':product})
                cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=True)
            return redirect('website:cart')



class cart_confirmation(View):
    def get(self, request):
        cart = Cart(request)
        for product in cart:
            checkItem = get_object_or_404(Item, pk=product['product'].pk)
            if checkItem.item_qty < product['quantity']:
                error_flag = 1
                cart_product_form = CartAddProductForm()
                total_price = cart.get_total_price()
                return render(request,'website/cart.html', {'cart':cart, 'cart_product_form': cart_product_form,'totalPrice':total_price,'error_flag':error_flag,'product':checkItem})
        return render(request,'website/orderconfirmation.html', {'cart':cart, })


class cart_order_done(View):
    def get(self, request):
        return render(request,'website/ordercomplete.html')
    def post(self,request):
        linenumber = 1
        cart = Cart(request)
        newOrder = Order(customer_first_name=request.POST['firstname'], customer_last_name=request.POST['lastname'],customer_email=request.POST['email'],customer_phone=request.POST['phone'],status='Received', payment_method=request.POST['payment'])
        newOrder.save()
        for product in cart:
            lineitem = LineItem(item=product['product'], line_number=linenumber, orderNumber=newOrder, qty=product['quantity'])
            linenumber = linenumber + 1
            changeItemQty = get_object_or_404(Item, pk=product['product'].pk)
            changeItemQty.sale(product['quantity'])
            changeItemQty.save()
            lineitem.save()
        cart.clear()
        #newOrder.order_received_email()
        return render(request,'website/ordercomplete.html')

