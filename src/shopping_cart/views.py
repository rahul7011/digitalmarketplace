from django.shortcuts import render, get_object_or_404, redirect
from books.models import Book, UserLibrary
from .models import OrderItem, Order, Payment
from django.http import HttpResponseRedirect
from django.conf import settings
import stripe
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return''.join(random.choices(string.ascii_uppercase + string.digits, k=15))


def add_to_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(book=book)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    # This http response redirects the response back to wherever it is coming from
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = get_object_or_404(OrderItem, book=book)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()
    # This http response redirects the response back to wherever it is coming from
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def order_view(request):
    order = get_object_or_404(Order, user=request.user)
    context = {
        'order': order
    }
    return render(request, "order_summary.html", context)


def checkout(request):
    order = get_object_or_404(Order, user=request.user)
    if request.method == "POST":

        # complete the order (reference code and set order to true)
        order.ref_code = create_ref_code()
        token=request.POST.get('stripeToken')
        # create a stripe charge
        charge = stripe.Charge.create(
            amount=int(order.get_total()*100),   #cents
            currency="usd",
            source=token,
            description=f"Chage for {request.user.username}",
        )
        
        # create a payment object and link to order
        payment=Payment()
        payment.order=order
        payment.stripe_charge_id=charge.id
        payment.total_amount=order.get_total()
        payment.save()
        # add the book to the users book list
        books=[item.book for item in order.items.all()]
        for book in books:
            request.user.userlibrary.books.add(book)
        order.is_ordered=True
        order.save()
        # # redirect to  users profile
        return redirect("/account/profile/")
    context={
        'order':order,
    }

    return render(request,"checkout.html",context)
