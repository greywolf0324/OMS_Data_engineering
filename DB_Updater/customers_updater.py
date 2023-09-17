import pandas as pd
from pathlib import Path

def customer_fields_updater():
    data = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_Customers.csv")
    OMS_Customer_Sales_Import = {
        "TaxRule*": "TaxRule",
        "Account": "SaleAccount",
        "PriceTier": "PriceTier",
        "Discount": "Discount",
        "SalesRepresentative*": "SalesRepresentative",
        "StockLocation": "Location",
        "CustomerContact": "ContactComment",
        "CustomerPhone": "Phone",
        "CustomerEmail": "Email",
        "Terms": "PaymentTerm"
    }

    res = {}

    keys = list(data["Name"])

    values = []

    for key in OMS_Customer_Sales_Import:
        values.append(list(data[OMS_Customer_Sales_Import[key]]))

    for i, key in enumerate(keys):
        temp = []

        for j in range(10):
            temp.append(values[j][i])

        res.update(
            {
                key: temp
            }
        )
    
    df = pd.DataFrame(res)

    df.to_csv(Path(__file__).resolve().parent.parent / "config/customer_fields.csv")

customer_fields_updater()