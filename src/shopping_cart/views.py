from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect,reverse
from books.models import Book, UserLibrary
from .models import OrderItem, Order, Payment
from django.http import HttpResponseRedirect,Http404
from django.conf import settings
import stripe
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
    return''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

@login_required
def add_to_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(book=book)
    order, created = Order.objects.get_or_create(user=request.user,is_ordered=False )
    order.items.add(order_item)
    order.save()
    messages.info(request,"Item successfully added to cart")
    # This http response redirects the response back to wherever it is coming from
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def remove_from_cart(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    order_item = get_object_or_404(OrderItem, book=book)
    order = get_object_or_404(Order, user=request.user,is_ordered=False)
    order.items.remove(order_item)
    order.save()
    messages.info(request,"Item successfully removed from cart")
    # This http response redirects the response back to wherever it is coming from
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def order_view(request):
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        context = {
            'order': order_qs[0]
        }
        return render(request, "order_summary.html", context)
    return render(request, "order_summary.html", {})

@login_required
def checkout(request):
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        raise Http404
    if request.method == "POST":

        try:
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
            messages.info(request,"Order has been placed successfully")
            # # redirect to  users profile
            return redirect("/account/profile/")

        #Send mail to yourself

        # Use Stripe's library to make requests...
        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
            messages.error(request,"There was a card error")
            return redirect(reverse("cart:checkout"))
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.error(request,"Too Many Payment request in very short amount of time")
            return redirect(reverse("cart:checkout"))
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.error(request,"Invalid Parameters have been provided")
            return redirect(reverse("cart:checkout"))
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.error(request,"There was a Authentication error")
            return redirect(reverse("cart:checkout"))
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.error(request,"There was a Network Communication failure ")
            return redirect(reverse("cart:checkout"))
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.error(request,"Some random error occured,Try again!")
            return redirect(reverse("cart:checkout"))
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            messages.error(request,"Something went wrong please try after some time")
            return redirect(reverse("cart:checkout"))

    context={
        'order':order,
    }

    return render(request,"checkout.html",context)
