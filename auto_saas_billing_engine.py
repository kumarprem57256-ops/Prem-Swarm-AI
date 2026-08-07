# Import required libraries
import datetime
import uuid
from decimal import Decimal

# Define a class for Customer
class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.subscriptions = []

    def add_subscription(self, subscription):
        self.subscriptions.append(subscription)

# Define a class for Subscription
class Subscription:
    def __init__(self, id, customer_id, plan_id, start_date, end_date):
        self.id = id
        self.customer_id = customer_id
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.charges = []

    def add_charge(self, charge):
        self.charges.append(charge)

# Define a class for Charge
class Charge:
    def __init__(self, id, subscription_id, amount, date):
        self.id = id
        self.subscription_id = subscription_id
        self.amount = Decimal(amount)
        self.date = date

# Define a class for Plan
class Plan:
    def __init__(self, id, name, price, currency):
        self.id = id
        self.name = name
        self.price = Decimal(price)
        self.currency = currency

# Define a class for BillingEngine
class BillingEngine:
    def __init__(self):
        self.customers = {}
        self.plans = {}

    def add_customer(self, customer):
        self.customers[customer.id] = customer

    def add_plan(self, plan):
        self.plans[plan.id] = plan

    def generate_invoice(self, customer_id, invoice_date):
        customer = self.customers.get(customer_id)
        if customer:
            invoice = {}
            invoice['customer_id'] = customer_id
            invoice['invoice_date'] = invoice_date
            invoice['charges'] = []
            for subscription in customer.subscriptions:
                for charge in subscription.charges:
                    invoice['charges'].append({
                        'subscription_id': subscription.id,
                        'charge_id': charge.id,
                        'amount': charge.amount,
                        'date': charge.date
                    })
            return invoice
        else:
            return None

    def process_payment(self, charge_id, payment_amount):
        charge = next((c for c in self.get_all_charges() if c.id == charge_id), None)
        if charge:
            if charge.amount <= payment_amount:
                return True
            else:
                return False
        else:
            return None

    def get_all_charges(self):
        charges = []
        for customer in self.customers.values():
            for subscription in customer.subscriptions:
                charges.extend(subscription.charges)
        return charges

# Create a billing engine
billing_engine = BillingEngine()

# Create customers
customer1 = Customer(str(uuid.uuid4()), 'John Doe', 'john@example.com')
customer2 = Customer(str(uuid.uuid4()), 'Jane Doe', 'jane@example.com')

# Create plans
plan1 = Plan(str(uuid.uuid4()), 'Basic', '9.99', 'USD')
plan2 = Plan(str(uuid.uuid4()), 'Premium', '19.99', 'USD')

# Add customers and plans to the billing engine
billing_engine.add_customer(customer1)
billing_engine.add_customer(customer2)
billing_engine.add_plan(plan1)
billing_engine.add_plan(plan2)

# Create subscriptions
subscription1 = Subscription(str(uuid.uuid4()), customer1.id, plan1.id, datetime.date(2022, 1, 1), datetime.date(2022, 12, 31))
subscription2 = Subscription(str(uuid.uuid4()), customer2.id, plan2.id, datetime.date(2022, 1, 1), datetime.date(2022, 12, 31))

# Add subscriptions to customers
customer1.add_subscription(subscription1)
customer2.add_subscription(subscription2)

# Create charges
charge1 = Charge(str(uuid.uuid4()), subscription1.id, '9.99', datetime.date(2022, 1, 15))
charge2 = Charge(str(uuid.uuid4()), subscription2.id, '19.99', datetime.date(2022, 1, 15))

# Add charges to subscriptions
subscription1.add_charge(charge1)
subscription2.add_charge(charge2)

# Generate invoice
invoice = billing_engine.generate_invoice(customer1.id, datetime.date(2022, 1, 31))
print(invoice)

# Process payment
payment_result = billing_engine.process_payment(charge1.id, 10.00)
print(payment_result)