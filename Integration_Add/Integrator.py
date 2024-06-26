import json
import pandas as pd
from csv import writer
from pathlib import Path


class Integrate_All:
    def __init__(self, customer_name) -> None:
        # Initialize productLib and UOM
        self.additional_uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv")
        self.length = 0
        self.currency = ""
        self.uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
        self.paymentterms = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
        self.OMS_Customer_Sales_Import = {
            "TaxRule*": "TaxRule",#Tax Exempt
            "Account": "SaleAccount",#4000
            "PriceTier": "PriceTier",#Tier 1 - Retail Pricing
            "Discount": "Discount",#0
            "SalesRepresentative*": "SalesRepresentative",#Jodie Pederson
            "StockLocation": "Location",#Houston Warehouse
            "CustomerContact": "ContactComment",#
            "CustomerPhone": "Phone",#
            "CustomerEmail": "Email",#
            "Terms": "PaymentTerm"#?    90 Days
        }
        self.customer_name = customer_name

    def auto_fun(self, customer_name):        
        customer_match = pd.read_csv(Path(__file__).resolve().parent.parent / "config/customer_fields.csv")
        
        values = list(customer_match[customer_name])
        print(values)
        auto_dic = {}

        # Account
        auto_dic.update({"Account": self.fun_iter_all(values[1])})

        #TaxRule*
        temp = []
        for _ in range(self.length):
            temp.append(values[0])
        
        auto_dic.update({"TaxRule*": self.fun_iter_all(values[0])})

        #Discount
        auto_dic.update({"Discount": self.fun_iter_line(values[3])})

        #rest [0, 3, 5, 6, 7, 8, 9]
        rest = [2, 4, 5, 6, 7, 8, 9]
        for i, field in enumerate(self.OMS_Customer_Sales_Import):
            if i in rest:
                temp = []
                temp.append(values[i])
                for _ in range(self.length - 1):
                    temp.append("")
                auto_dic.update({field: temp})
            
        return auto_dic
    
    def fun_iter_all(self, input):
        temp = []
        
        for _ in range(self.length):
            temp.append(input)
        
        return temp
    
    def fun_iter_top(self, input):
        temp = [input]

        for _ in range(self.length - 1):
            temp.append("")

        return temp
    
        
    def fun_iter_line(self, input):
        temp = []
        temp.append("")

        for _ in range(self.length - 1):
            temp.append(input)
        
        return temp
    
    def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
        shippingnotes = [m_shipdates[0] + "-" + m_canceldates[0]]
        for i in range(1, self.length):
            shippingnotes.append("")
        
        return shippingnotes
    
    def fun_invoicedata_expiredate(self, m_shipdates: str):
        temp = []
        if self.currency == "usd":
            temp.append("/".join(m_shipdates[0].split(".")[::-1]))
        else:
            temp.append("/".join(m_shipdates[0].split("/")[::-1]))
        for _ in range(self.length - 1):
            temp.append("")
        
        return temp

    def fun_total(self, quantity, price_amount):
        total = [""]

        for i in range(1, self.length):
            total.append(quantity[i] * price_amount[i])

        return {"Total*": total}

    def fun_invoice(self):
        temp = []
        temp.append("invoice")
        for _ in range(self.length - 1):
            temp.append("invoicelines")

        return {"RecordType*": temp}
    
    def fun_remove_space(self, st):
        st = st.replace(" ", "")

        return st

class Integrate_All(Integrate_All):
    def re_init(self):
        self.additional_uom = pd.read_csv("config/uom_sku.csv")

    
        
    #Define several Integrate_funs that is needed for SalesImport
    def fun_Price_Amount(self, m_qty_ordered, m_unit_price):
        price_amount = []
        
        for i in range(1, self.length):
            if m_qty_ordered[i] == '': m_qty_ordered[i] = '0'
            if m_unit_price[i] == '': m_unit_price[i] = '0'
            price_amount.append(float(m_qty_ordered[i]) * (float(m_unit_price[i])))
        
        price_amount.insert(0, "")
        
        return price_amount
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def Integrate_final(self, matching_res, currency):
        self.currency = currency
        SalesImport = []
        for i in range(len(matching_res)):
            SalesImport.append({})
        
        for i, element in enumerate(matching_res):
            #everything will be done here

            self.length = len(element[list(element.keys())[0]])

            # Create formula fields
            SalesImport[i].update(
                {
                    "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
                    "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
                    "YourBaseCurrency*": self.fun_iter_top(element["Currency"][0]),
                    "CustomerCurrency*": self.fun_iter_top(element["Currency"][0]),
                    
                }
            )
            SalesImport[i].update(
                {
                    "ShippingAddressLine1*": element["Ship To Address 1"],
                    "ShippingCity*": element["Ship To City"],
                    "ShippingProvince*": element["Ship To State"],
                    "ShippingPostcode*": element["Ship to Zip"],
                    "ShippingCountry*": element["Ship To Country"],
                    "BillingAddressLine1*": element["Buying Party Name"],
                }
            )
            #customername
            #Add OMS_CustomerName addition functionality
            #frontend input here
            # lis_customer = [i for i in range(49)] 
            # with open("config/OMS_DB/OMS_Customers.csv", "a") as f:
            #     writer_object = writer(f)

            #     writer_object.writerow(lis_customer)
            #     f.close()

            
            
            
            SalesImport[i].update(
                {
                    "CustomerName*": self.fun_iter_all(self.customer_name),
                }
            )

            # Add InvoiceNumber*
            SalesImport[i].update(
                {
                    "InvoiceNumber*": self.fun_iter_all(element["Retailers PO"][0])
                }
            )
            # Add customername inherited fields
            SalesImport[i].update(self.auto_fun(self.customer_name))
            
            # Add RecordType
            SalesImport[i].update(self.fun_invoice())

            # Add [Product*, quantity*, Price/Amount], Total*
            product = {"Product*": [""]}
            quantity = {"Quantity*": [""]}
            price = {"Price/Amount*": [""]}

            def vendor_addition(input, num):
                product["Product*"].append(self.additional_uom[element["Vendor Style"][k]][0])
                quantity["Quantity*"].append(int(float(input["Qty Ordered"][num])) / int(float(self.additional_uom[element["Vendor Style"][k]][1])))
                price["Price/Amount*"].append(float(self.fun_remove_space(input["Unit Price"][num])) * int(self.additional_uom[element["Vendor Style"][k]][1]))

            for k in range(1, self.length):
                # if element["Vendor Style"][k] in self.additional_uom.keys():
                vendor_addition(element, k)
                product["Product*"].append(self.additional_uom[element["Vendor Style"][k]][0])
                quantity["Quantity*"].append(int(float(self.fun_remove_space(str(element["Qty Ordered"][k])))) / int(float(self.fun_remove_space(str(self.additional_uom[element["Vendor Style"][k]][1])))))
                price["Price/Amount*"].append(float(self.fun_remove_space(element["Unit Price"][k])) * int(self.additional_uom[element["Vendor Style"][k]][1]))
                
                # else:
                    # self.new_sku.append(element["Vendor Style"][k])
                    #frontend input here
                    # lis_aduom = [i for i in range(9)]
                    # with open("config/OMS_DB/OMS_AdditionalUOM.csv", "a") as f:
                    #     writer_object = writer(f)

                    #     writer_object.writerow(lis_aduom)
                    #     f.close()
                    
                    # self.re_init()
                    # vendor_addition(element, k)
            
            SalesImport[i].update(product)
            SalesImport[i].update(quantity)
            SalesImport[i].update(price)
            SalesImport[i].update(self.fun_total(quantity["Quantity*"], price["Price/Amount*"]))

            if SalesImport[i]["CustomerCurrency*"][0] == SalesImport[i]["YourBaseCurrency*"][0]:
                temp = [""]
                for _ in range(self.length - 1):
                    temp.append(1)
                SalesImport[i].update(
                    {
                        "CurrencyConversionRate": temp
                    }
                )
            else:
                #input through input box(make currency rate functionality)
                pass

            # if element["Frt Terms"] == "":
            #     #This is temporary plan to avoid non-value!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #     SalesImport[i].update(
            #         {
            #             "Terms": element["Frt Terms"]
            #         }
            #     )
            #     #make input box to input Frt Terms
            #     #frontend input here
            #     # lis_payment = [i for i in range(2, 7)]
            #     # with open("config/OMS_DB/OMS_PaymentTerm.csv") as f:
            #     #     writer_object = writer(f)

            #     #     writer_object.writerow(lis_payment)
            #     #     f.close()
            #     pass
            
            # else:
            #     # if element["Frt Terms"] in list(self.paymentterms["Name"]):
            #     SalesImport[i].update(
            #         {
            #             "Terms": element["Frt Terms"]
            #         }
            #     )
            #     # else:
            #     #     self.new_paymentterm.append(element["Frt Terms"])
            #         #OMS_Paymentterm addition
            #         # lis_payment = [1, 2, 3, 4, 5, 6] #frontend input here
            #         # with open("config/OMS_DB/OMS_PaymentTerm.csv", "a") as f:
            #         #     writer_object = writer(f)

            #         #     writer_object.writerow(lis_payment)
            #         #     f.close()
                    
            #         # SalesImport[i].update(
            #         #     {
            #         #         "Terms": element["Frt Terms"]
            #         #     }
            #         # )
        print(SalesImport)
        return SalesImport

# class PEPCO_Integrate_All(Integrate_All):
#     def __init__(self) -> None:
#         # Initialize productLib and UOM
#         self.additional_uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/uom_sku.csv")
#         self.length = 0
#         self.currency = ""
#         self.uom = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
#         self.paymentterms = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
#         self.OMS_Customer_Sales_Import = {
#             "TaxRule*": "TaxRule",
#             "Account": "SaleAccount",
#             "PriceTier": "PriceTier",
#             "Discount": "Discount",
#             "SalesRepresentative*": "SalesRepresentative",
#             "StockLocation": "Location",
#             "CustomerContact": "ContactComment",
#             "CustomerPhone": "Phone",
#             "CustomerEmail": "Email",
#             "Terms": "PaymentTerm"
#         }

#     def match_plain(self, input):
#         res = []
#         for i, _ in enumerate(input):
#             res.append(input[f"PDF{i}"])

#         return res
    
#     def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
#         shippingnotes = [m_shipdates + "-" + m_canceldates]
#         for i in range(1, self.length):
#             shippingnotes.append("")
        
#         return shippingnotes
    
#     def Integrate_final(self, PO_res, currency):
#         self.currency = currency
#         print(PO_res, "---------------------------------")
#         SalesImport = []
        
#         input = self.match_plain(PO_res)

#         for i in range(len(input)):
#             SalesImport.append({})

#         for i, element in enumerate(input):
#             self.length = 2
#             # Create formula fields
            
#             if currency == "eur":
#                 SalesImport[i].update(
#                     {
#                         "ShippingNotes": self.fun_shippingnotes(element["Booking date"], element["Handover date"]),
#                         "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate([element["Handover date"]]),
#                         "YourBaseCurrency*": self.fun_iter_all(element["Purchase price"].split(" ")[1]),
                        
#                     }
#                 )
#             else:
#                 SalesImport[i].update(
#                     {
#                         "ShippingNotes": self.fun_shippingnotes(element["Booking date"], element["Handover date"]),
#                         "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate([element["Handover date"]]),
#                         "YourBaseCurrency*": self.fun_iter_all("USD"),
                        
#                     }
#                 )
#             SalesImport[i].update(
#                     {
#                         "CustomerCurrency*": SalesImport[i]["YourBaseCurrency*"]
#                     }
#                 )
#             customer_name = "Pepco - "
#             if element["Purchase price"].split(" ")[1] == "EUR" or element["Purchase price"].split(" ")[1] == "USD":
#                 customer_name = customer_name + element["Purchase price"].split(" ")[1]

#             else:
#                 customer_name = customer_name + "RMB"
            
#             SalesImport[i].update(
#                 {
#                     "CustomerName*": self.fun_iter_all(customer_name),
#                 }
#             )
#             # Add InvoiceNumber*
#             SalesImport[i].update(
#                 {
#                     "InvoiceNumber*": [element["Order - ID"], element["Order - ID"]]
#                 }
#             )

#             # Add customername inherited fields
#             SalesImport[i].update(self.auto_fun(customer_name))

#             # Add RecordType
#             SalesImport[i].update(self.fun_invoice())

#             # Add [Product*, quantity*, Price/Amount], Total*
#             product = {"Product*": [""]}
#             quantity = {"Quantity*": [""]}
#             price = {"Price/Amount*": [""]}

#             product["Product*"].append("")
#             quantity["Quantity*"].append(int(float(element["Total"])) / int(float(element["Total qty in outer"])))
#             st = element["Purchase price"]
#             print(st, "------------------")
#             if currency == "eur":
#                 price["Price/Amount*"].append(float(st.split(" ")[0].split(",")[0] + "." + st.split(" ")[0].split(",")[1]) * int(float(element["Total qty in outer"])))
#             else:
#                 price["Price/Amount*"].append(float((st.split(",")[0] + "." + st.split(",")[1]).replace(" ", "")) * int(float(element["Total qty in outer"])))
#             SalesImport[i].update(product)
#             SalesImport[i].update(quantity)
#             SalesImport[i].update(price)
#             SalesImport[i].update(self.fun_total(quantity["Quantity*"], price["Price/Amount*"]))

#             temp = ["", 1]

#             SalesImport[i].update(
#                     {
#                         "CurrencyConversionRate": temp
#                     }
#                 )
            
#         return SalesImport
