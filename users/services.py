import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    product = stripe.Product.create(name=course.title)

    return product.get('name')


def create_stripe_price(amount):
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Course_payment"},
    )




def create_stripe_sessions(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )

    return session.get('id'), session.get('url')
