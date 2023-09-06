import json
import pandas as pd
from csv import writer

class Integreate_All:
    def __init__(self) -> None:
        # Initialize productLib and UOM
        self.additional_uom = pd.read_csv("config/uom_sku.csv")
        self.length = 0
        self.uom = pd.read_csv("config/OMS_DB/OMS_UOM.csv")
        self.paymentterms = pd.read_csv("config/OMS_DB/OMS_PaymentTerm.csv")

    def re_init(self):
        self.additional_uom = pd.read_csv("config/uom_sku.csv")

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
        total = [""]

        for i in range(1, self.length):
            # print("@@@@@")
            total.append(quantity[i] * price_amount[i])

        return {"Total*": total}
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def fun_shippingnotes(self, m_shipdates: str, m_canceldates: str):
        shippingnotes = [m_shipdates[0] + "-" + m_canceldates[0]]
        for i in range(1, self.length):
            shippingnotes.append("")
        
        return shippingnotes
    
    def fun_invoicedata_expiredate(self, m_shipdates: str):
        return m_shipdates
    
    def fun_iter_all(self, input):
        temp = []
        
        for _ in range(self.length):
            temp.append(input)
        
        return temp
    
    def fun_iter_line(self, input):
        temp = []
        temp.append("")

        for _ in range(self.length - 1):
            temp.append(input)
        
        return temp
    
    def fun_invoice(self):
        temp = []
        temp.append("invoice")
        for _ in range(self.length - 1):
            temp.append("invoiceline")

        return {"RecordType*": temp}
    
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
                    "ShippingNotes": self.fun_shippingnotes(element["Ship Dates"], element["Cancel Date"]),
                    "InvoiceDate*/ExpireDate": self.fun_invoicedata_expiredate(element["Ship Dates"]),
                    "YourBaseCurrency*": self.fun_iter_all("USD"),
                    
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

            
            
            customer_name = "BUC-EE'S"
            SalesImport[i].update(
                {
                    "CustomerName*": self.fun_iter_all(customer_name),
                }
            )

            # Add customername inherited fields
            SalesImport[i].update(self.auto_fun(customer_name))
            
            # Add RecordType
            SalesImport[i].update(self.fun_invoice())

            # Add [Product*, quantity*, Price/Amount], Total*
            product = {"Product*": [""]}
            quantity = {"Quantity*": [""]}
            price = {"Price/Amount*": [""]}

            def vendor_addition(input, num):
                product["Product*"].append(self.additional_uom[input["Vendor Style"][num]][0])
                # print(input["Qty Ordered"][num])
                # print(self.additional_uom[input["Vendor Style"][num]][1])
                quantity["Quantity*"].append(int(float(input["Qty Ordered"][num])) / int(float(self.additional_uom[input["Vendor Style"][num]][1])))
                price["Price/Amount*"].append(float(input["Unit Price"][num]) * int(self.additional_uom[input["Vendor Style"][num]][1]))

            for k in range(1, self.length):
                # print(element["Vendor Style"][k])
                if element["Vendor Style"][k] in self.additional_uom.keys():
                    print("okay!")
                    vendor_addition(element, k)
                    product["Product*"].append(self.additional_uom[element["Vendor Style"][k]][0])
                    # print(element["Qty Ordered"][k])
                    # print(self.additional_uom[element["Vendor Style"][k]][1])
                    quantity["Quantity*"].append(int(float(element["Qty Ordered"][k])) / int(float(self.additional_uom[element["Vendor Style"][k]][1])))
                    price["Price/Amount*"].append(float(element["Unit Price"][k]) * int(self.additional_uom[element["Vendor Style"][k]][1]))
                
                else:
                    print("#########################################")
                    #frontend input here
                    lis_aduom = [i for i in range(9)]
                    with open("config/OMS_DB/OMS_AdditionalUOM.csv", "a") as f:
                        writer_object = writer(f)

                        writer_object.writerow(lis_aduom)
                        f.close()
                    
                    self.re_init()
                    vendor_addition(element, k)
            
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

            if element["Frt Terms"] == "":
                #make input box to input Frt Terms
                #frontend input here
                lis_payment = [i for i in range(2, 7)]
                with open("config/OMS_DB/OMS_PaymentTerm.csv") as f:
                    writer_object = writer(f)

                    writer_object.writerow(lis_payment)
                    f.close()
            
            else:
                if element["Frt Terms"] in list(self.paymentterms["Name"]):
                    SalesImport[i].update(
                        {
                            "Terms": element["Frt Terms"]
                        }
                    )
                else:
                    #OMS_Paymentterm addition
                    lis_payment = [1, 2, 3, 4, 5, 6] #frontend input here
                    with open("config/OMS_DB/OMS_PaymentTerm.csv", "a") as f:
                        writer_object = writer(f)

                        writer_object.writerow(lis_payment)
                        f.close()
                    
                    SalesImport[i].update(
                        {
                            "Terms": element["Frt Terms"]
                        }
                    )
        
        return SalesImport
