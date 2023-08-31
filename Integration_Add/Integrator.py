import json
import pandas as pd


class Integreate_All:
    def __init__(self) -> None:
        # Initialize productLib and UOM
        UOM = pd.read_csv("config/UOM.csv")
        self.length = 0
        
        product_lib = ""
        pass
    
    def auto_fun(self, customer_name):
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
        
        customer_match = pd.read_csv("config/customer_fields.csv")
        
        values = list(customer_match[customer_name])
        auto_dic = {}

        # Account
        temp = []
        for _ in range(self.length):
            temp.append(values[2])
        
        auto_dic.update({"Account": temp})

        #TaxRule*
        temp = []
        for _ in range(self.length):
            temp.append(values[1])
        
        auto_dic.update({"TaxRule*": temp})

        #Discount
        temp = []
        temp.append("")
        for _ in range(self.length - 1):
            temp.append(values[4])
        
        auto_dic.update({"Discount": temp})

        #rest [0, 3, 5, 6, 7, 8, 9]
        rest = [0, 3, 5, 6, 7, 8, 9]
        for i, field in enumerate(OMS_Customer_Sales_Import):
            if i in rest:
                temp = []
                temp.append(values[i])
                for _ in range(self.length - 1):
                    temp.append("")
                auto_dic.update({field: temp})
            
        return auto_dic
        
    #Define several Integrate_funs that is needed for SalesImport
    def fun_Price_Amount(self, m_qty_ordered, m_unit_price):
        price_amount = []
        
        for i in range(1, self.length):
            # print(m_qty_ordered[i], m_unit_price[i])
            if m_qty_ordered[i] == '': m_qty_ordered[i] = '0'
            if m_unit_price[i] == '': m_unit_price[i] = '0'
            price_amount.append(float(m_qty_ordered[i]) * (float(m_unit_price[i])))
        
        price_amount.insert(0, "")
        
        return price_amount
    
    def fun_total(self, quantity, price_amount):
        total = []

        for i in range(1, self.length):
            total.append(quantity[i] * price_amount[i])

        total.insert(0, "")

        return total
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
        shippingnotes = [m_shipdates[0] + "-" + m_canceldates[0]]
        for i in range(1, self.length):
            shippingnotes.append("")
        
        return shippingnotes
    
    def fun_invoicedata_expiredate(self, m_shipdates: str):
        return m_shipdates
    
    def fun_iteration(self, input):
        temp = []
        
        for _ in range(self.length):
            temp.append(input)
        
        return temp
    
    def Integrate_final(self, matching_res):
        SalesImport = []
        # print(len(matching_res))
        for i in range(len(matching_res)):
            SalesImport.append({})
        
        for i, element in enumerate(matching_res):
            #everything will be done here
            # print(element["Qty Ordered"], element["Unit Price"])
            # print(list(element.keys())[0])
            self.length = len(element[list(element.keys())[0]])
            # print(self.length)
            # Create formula fields

            SalesImport[i].update(
                {
                    "Price/Amount*": self.fun_Price_Amount(element["Qty Ordered"], element["Unit Price"]),
                    "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
                    "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
                    "YourBaseCurrency*": self.fun_iteration("USD"),
                    
                }
            )
            # print(SalesImport)
            SalesImport[i].update(
                {
                    "CustomerName*": self.fun_iteration("BUC-EE'S"),
                }
            )

            # Add inherited fields
            SalesImport[i].update(self.auto_fun("BUC-EE'S"))
            
        
        
        return SalesImport
