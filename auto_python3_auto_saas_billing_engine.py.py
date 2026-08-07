# Import required libraries
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Define a class for the billing engine
class BillingEngine:
    def __init__(self):
        self.billing_data = {}

    # Method to add a new customer
    def add_customer(self, customer_id: str, subscription_id: str, plan: str, start_date: str, end_date: str):
        self.billing_data[customer_id] = {
            "subscription_id": subscription_id,
            "plan": plan,
            "start_date": start_date,
            "end_date": end_date,
            "charges": []
        }

    # Method to add a new charge
    def add_charge(self, customer_id: str, amount: float, description: str, date: str):
        if customer_id in self.billing_data:
            self.billing_data[customer_id]["charges"].append({
                "amount": amount,
                "description": description,
                "date": date
            })
        else:
            print(f"Customer {customer_id} not found.")

    # Method to generate invoice
    def generate_invoice(self, customer_id: str):
        if customer_id in self.billing_data:
            customer_data = self.billing_data[customer_id]
            invoice_data = {
                "customer_id": customer_id,
                "subscription_id": customer_data["subscription_id"],
                "plan": customer_data["plan"],
                "start_date": customer_data["start_date"],
                "end_date": customer_data["end_date"],
                "charges": customer_data["charges"]
            }
            return invoice_data
        else:
            print(f"Customer {customer_id} not found.")

    # Method to calculate total charges
    def calculate_total_charges(self, customer_id: str):
        if customer_id in self.billing_data:
            customer_data = self.billing_data[customer_id]
            total_charges = sum(charge["amount"] for charge in customer_data["charges"])
            return total_charges
        else:
            print(f"Customer {customer_id} not found.")

# Define a function to process billing data
def process_billing_data(billing_engine: BillingEngine, data: Dict):
    for customer in data["customers"]:
        billing_engine.add_customer(customer["id"], customer["subscription_id"], customer["plan"], customer["start_date"], customer["end_date"])
        for charge in customer["charges"]:
            billing_engine.add_charge(customer["id"], charge["amount"], charge["description"], charge["date"])

# Define a function to generate invoices
def generate_invoices(billing_engine: BillingEngine, customer_ids: List[str]):
    invoices = []
    for customer_id in customer_ids:
        invoice = billing_engine.generate_invoice(customer_id)
        invoices.append(invoice)
    return invoices

# Define a function to calculate total charges
def calculate_total_charges(billing_engine: BillingEngine, customer_ids: List[str]):
    total_charges = {}
    for customer_id in customer_ids:
        total_charges[customer_id] = billing_engine.calculate_total_charges(customer_id)
    return total_charges

# Example usage
if __name__ == "__main__":
    billing_engine = BillingEngine()

    # Sample billing data
    data = {
        "customers": [
            {
                "id": "customer1",
                "subscription_id": "subscription1",
                "plan": "plan1",
                "start_date": "2022-01-01",
                "end_date": "2022-12-31",
                "charges": [
                    {"amount": 10.99, "description": "Charge 1", "date": "2022-01-15"},
                    {"amount": 20.99, "description": "Charge 2", "date": "2022-02-15"}
                ]
            },
            {
                "id": "customer2",
                "subscription_id": "subscription2",
                "plan": "plan2",
                "start_date": "2022-01-01",
                "end_date": "2022-12-31",
                "charges": [
                    {"amount": 30.99, "description": "Charge 3", "date": "2022-03-15"},
                    {"amount": 40.99, "description": "Charge 4", "date": "2022-04-15"}
                ]
            }
        ]
    }

    process_billing_data(billing_engine, data)

    customer_ids = ["customer1", "customer2"]
    invoices = generate_invoices(billing_engine, customer_ids)
    print(json.dumps(invoices, indent=4))

    total_charges = calculate_total_charges(billing_engine, customer_ids)
    print(json.dumps(total_charges, indent=4))