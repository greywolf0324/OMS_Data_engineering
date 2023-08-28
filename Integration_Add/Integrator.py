import json
import pandas as pd


class Integreate_All:
    def __init__(self) -> None:
        # Initialize productLib and UOM
        UOM = pd.read_csv("UOM.csv")
        
        
        product_lib = ""
        pass
    
    def auto_fun(self, name):
        OMS_Customer_Sales_Import = {
            "CustomerCurrency*": "Currency",
            "TaxRule*": "TaxRule",
            "Account": "SaleAccount",
            "PriceTier": "PriceTier",
            "Discount": "Discount",
            "SalesRepresentative*": "SalesRepresentative",
            "StockLocation": "Location",
            "CustomerContact": "ContactComment",
            "CustomerPhone": "Phone",
            "CustomerEmail": "Email",    
        }
        
        customer_match = pd.read_csv("customer_fields.csv")
        
        values = list(customer_match[name])
        auto_dic = {}
        
        for i, field in enumerate(OMS_Customer_Sales_Import):
            auto_dic.update({field: values[i]})
            
        return auto_dic
        
    #Define several Integrate_funs that is needed for SalesImport
    def fun_Price_Amount(self, m_qty_ordered, m_unit_price):
        return float(m_qty_ordered) * float(m_unit_price)
    
    def fun_total(self, quantity, price_amount):
        return quantity * price_amount
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
        return m_shipdates + "-" + m_canceldates
    
    def fun_invoicedata_expiredate(self, m_shipdates: str):
        return m_shipdates
    
    def Integrate_final(self, matching_res):
        SalesImport = []
        # print(len(matching_res))
        for i in range(len(matching_res)):
            SalesImport.append({})
        
        for i, element in enumerate(matching_res):
            #everything will be done here
            # print(element["Qty Ordered"], element["Unit Price"])

            # Create formula fields
            SalesImport[i].update(
                {
                    "Price/Amount*": self.fun_Price_Amount(element["Qty Ordered"], element["Unit Price"]),
                    "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
                    "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
                    "YourBaseCurrency*": "USD",
                    
                }
            )

            SalesImport[i].update(
                {
                    "CustomerName*": "BUC-EE'S",
                }
            )

            # Add inherited fields
            SalesImport[i].update(self.auto_fun("BUC-EE'S"))
            
        
        
        return SalesImport
