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
        return m_qty_ordered * m_unit_price
    
    def fun_total(self, quantity, price_amount):
        return quantity * price_amount
    
    def fun_invoicenumber(self, m_po_number):
        return m_po_number
    
    def Integrate_All(self, matching_res):
        SalesImport = self.Integrate_funs(matching_res)
        
        return SalesImport
    

    "RecordType*",
    "CustomerName*",
    "InvoiceNumber*",
    "Reference/Comment/Note",
    "Product*",
    "Quantity*",
    "Price/Amount*" = "Qty Ordered" * ""
    "Discount",
    "Tax",
    "Total*",
    "Account",
    "TaxRule*",
    "DropShip",
    "CurrencyConversionRate",
    "DatePaid*",
    "CustomerContact",
    "CustomerPhone",
    "CustomerEmail",
    "SalesRepresentative*",
    "ShipmentRequiredByDate",
    "YourBaseCurrency*",
    "CustomerCurrency*",
    "Terms",
    "PriceTier",
    "StockLocation",
    "MemoOnInvoice",
    "InvoiceDate*/ExpireDate",
    "InvoiceDueDate",
    "TaxInclusive*",
    "ShippingAddressLine1*",
    "ShippingAddressLine2",
    "ShipToOther*",
    "ShippingCity*",
    "ShippingProvince*",
    "ShippingPostcode*",
    "ShippingCountry*",
    "ShipToCompany*",
    "BillingAddressLine1*",
    "BillingAddressLine2",
    "BillingCity*",
    "BillingProvince*",
    "BillingPostcode*",
    "BillingCountry*",
    "CreditNoteNumber",
    "CreditNoteDate",
    "CustomField1",
    "CustomField2",
    "CustomField3",
    "CustomField4",
    "CustomField5",
    "CustomField6",
    "CustomField7",
    "CustomField8",
    "CustomField9",
    "CustomField10",
    "CarrierCode",
    "CarrierServiceCode",
    "ShipToContact",
    "ShippingNotes"