import pandas as pd
from pathlib import Path
import math
import numpy as np

class Extractor:
    def __init__(self) -> None:
        self.OMS_AdditionalUOM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
        self.OMS_Customers = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_Customers.csv")
        self.OMS_InventoryList = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_InventoryList.csv")
        self.OMS_PaymentTerm = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_PaymentTerm.csv")
        self.OMS_UoM = pd.read_csv(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_UOM.csv")
        self.length = 0

    def extractor(self, matching_res):
        equal_additional_uom = []
        equal_inventorylist = []

        for content in matching_res:
            self.length = len(content.keys())

            temp_additional = {}
            temp_inventory = {}

            for key in self.OMS_AdditionalUOM:
                temp_additional.update(
                    {
                        key: []
                    }
                )

            for key in self.OMS_InventoryList:
                temp_inventory.update(
                    {
                        key: []
                    }
                )

            for sku in list(self.OMS_AdditionalUOM["BaseSKU"]):
                if sku in list(content["Vendor Style"])[1:]:
                    for i, key in enumerate(temp_additional):
                        value = self.OMS_AdditionalUOM[self.OMS_AdditionalUOM["BaseSKU"] == sku].iloc[0].values[i]
                        # print(type(self.OMS_AdditionalUOM[self.OMS_AdditionalUOM["BaseSKU"] == sku].iloc[0].values[i]))
                        if type(value) == np.float64:
                            if math.isnan(value):
                                temp_additional[key].append("")
                        
                        elif type(value) == np.bool_:
                            temp_additional[key].append(bool(value))

                        elif type(value) == np.int64:
                            temp_additional[key].append(int(value))
                        else:
                            temp_additional[key].append(value)

                    # print(temp_additional)
                    # for key in self.OMS_AdditionalUOM[self.OMS_AdditionalUOM["BaseSKU"] == sku]:
                    #     print(type(self.OMS_AdditionalUOM[self.OMS_AdditionalUOM["BaseSKU"] == sku][key]))
            equal_additional_uom.append(temp_additional)
            
            for product_ in list(self.OMS_InventoryList["ProductCode"]):
                for product in list(content["Vendor Style"])[1:]:
                    if type(product) != str: product = str(product)
                    if type(product_) != str: product_ = str(product_)
                    if product in product_ and product != "":
                        for i, key in enumerate(temp_inventory):
                            # print(type(self.OMS_InventoryList[self.OMS_InventoryList["ProductCode"] == sku].iloc[0].values[i]))
                            value = self.OMS_InventoryList[self.OMS_InventoryList["ProductCode"] == product_].iloc[0].values[i]
                            if type(value) == np.float64 or type(value) == float:
                                if math.isnan(value):
                                    temp_inventory[key].append("")
                                else:
                                    temp_inventory[key].append(float(value))
                            elif type(value) == np.bool_:
                                temp_inventory[key].append(bool(value))
                            elif type(value) == np.int64:
                                    temp_inventory[key].append(int(value))
                            else:
                                temp_inventory[key].append(value)

            equal_inventorylist.append(temp_inventory)
        return {
            "OMS_AdditionalUOM": equal_additional_uom,
            "OMS_InventoryList": equal_inventorylist
        }