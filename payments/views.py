from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import stripe
from .models import Payment
from orders.models import Order
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        user = request.user if request.user.is_authenticated else None
        order = Order.objects.get(id=data.get("order_id")) if data.get("order_id") else None

        if order is None:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            
        if order.status == 'Completed':
            return Response({"error": "Order already completed."}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = int(order.quantity * order.product.price * 100 )
        currency = 'usd'


        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": currency,
                            "product_data": {
                                "name": order.product.name,
                                "description": order.product.description
                                },
                            "unit_amount": amount,
                        },
                        "quantity": order.quantity,
                    },
                ],
                mode="payment",
                success_url=f"{settings.DOMAIN}/api/v1/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN}/api/v1/payments/failed",
            )



            # Create Payment record
            payment = Payment.objects.create(
                user=user,
                amount=amount / 100,
                stripe_payment_intent_id=session["id"],
                currency=currency,
                order= Order.objects.get(id=data.get("order_id"))
            )
            order.status = 'In Progress'
            order.save()

            return Response({"checkout_url": session["url"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccess(APIView):
    def get(self, request):
        session_id = request.GET.get("session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = session.get("id")
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent)
            payment.status = 'completed'
            payment.save()

            order = payment.order
            order.status = 'Completed'
            order.save()

            

            return Response({"message": "Payment successful!"}, status=status.HTTP_200_OK)
        except stripe.error.InvalidRequestError:
            return Response({"error": "Invalid session ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)


class PaymentFailed(APIView):
    def get(self, request):
        return Response({"message": "Payment failed!"}, status=status.HTTP_200_OK)