import pandas as pd
from csv import writer

class Udpater:
    def __init__(self) -> None:
        pass
    
    def initializer(self, file_name):
        f = open(file_name, "w+")
        f.close()

    def updater(self, new_DB: dict):
        #OMS udpate
        with open("config/OMS_DB/OMS_AdditionalUOM.csv", "a") as f:
            for line in new_DB["OMS_AdditionalUOM"]:
                writer_object = writer(f)
                writer_object.writerow(line)
                f.close()
        
        with open("config/OMS_DB/OMS_PaymentTerm.csv") as f:
            for line in new_DB["OMS_PaymentTerm"]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        
        with open("config/OMS_DB/OMS_InventoryList.csv", "a") as f:
            for line in new_DB["OMS_InventoryList"]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        
        with open("config/OMS_DB/OMS_UOM.csv", "a") as f:
            df_uom = pd.read_csv("config/OMS_DB/OMS_UOM.csv")
            writer_object = writer(f)
            df = pd.read_csv("OMS_AdditionalUOM.csv")
            lis = df["AdditionalUnitsOfMeasureName"]

            temp_set = set(lis)

            for item in temp_set:
                if item not in list(df_uom["Name"]):
                    writer_object.writerow([item])

        #uom_sku udpate
        UOM = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")
        uom = UOM[["BaseSKU", "AdditionalUnitsOfMeasureSKU", "NumberOfBaseUnitsInAdditionalUnit"]]
        keys = list(uom["BaseSKU"])

        dic = {}

        for i, key in enumerate(keys):
          dic.update({key: [uom["AdditionalUnitsOfMeasureSKU"][i], uom["NumberOfBaseUnitsInAdditionalUnit"][i]]})

        self.initializer("uom_sku.csv")

        df = pd.DataFrame(dic)
        df.to_csv("uom_sku.csv")