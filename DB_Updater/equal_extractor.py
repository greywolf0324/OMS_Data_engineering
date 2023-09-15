import pandas as pd
from pathlib import Path



class Extractor:
    def __init__(self) -> None:
        self.OMS_AdditionalUOM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
        self.OMS_Customers = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_Customers.csv")
        self.OMS_InventoryList = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv")
        self.OMS_PaymentTerm = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
        self.OMS_UoM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
        self.length = 0

    def extractor(self, matching_res):
        equal_additional_uom = {}
        equal_inventorylist = {}


        for content in matching_res:
            self.length = len(content.keys())

            for sku in list(self.OMS_AdditionalUOM["BaseSKU"]):
                if sku in list(content["Vendor Style"])[1:]:
                    equal_additional_uom.update(self.OMS_AdditionalUOM[self.OMS_AdditionalUOM["BaseSKU"] == sku])
            
            for product_ in list(self.OMS_InventoryList["ProductCode"]):
                for product in list(content["Vendor Style"])[1:]:
                    if product in product_:
                        equal_inventorylist.update(self.OMS_InventoryList[self.OMS_InventoryList["BaseSKU"] == product_])
        
        return {
            "OMS_AdditionalUOM": equal_additional_uom,
            "OMS_InventoryList": equal_inventorylist
        }