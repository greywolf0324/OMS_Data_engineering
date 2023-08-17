import json
import pandas as pd


class Integreate_All:
    def __init__(self) -> None:
        # Initialize productLib and UOM
        
        
        product_lib = ""
        UOM = ""
        pass
    
    #Define several Integrate_funs that is needed for SalesImport
    def fun_Price_Amount(self, m_qty_ordered, m_unit_price):
        return float(m_qty_ordered) * float(m_unit_price)
    
    def fun_total(self, quantity, price_amount):
        return quantity * price_amount
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def Integrate_final(self, matching_res):
        SalesImport = []
        print(len(matching_res))
        for i in range(len(matching_res)):
            SalesImport.append({})
        
        for i, element in enumerate(matching_res):
            #everything will be done here
            SalesImport[i].update({"Price/Amount*": self.fun_Price_Amount(element["Qty Ordered"], element["Unit Price"])})
            
        
        
        return SalesImport
