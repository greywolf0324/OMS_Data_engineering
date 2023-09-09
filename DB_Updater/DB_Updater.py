import pandas as pd
from csv import writer

class Udpater:
    def __init__(self) -> None:
        pass
    
    def elaborator(self, file_name):
        # self.elaborator(Path(__file__).resolve().parent.parent / "config/OMS_DB/OMS_AdditionalUOM.csv")
        temp_df = pd.read_csv(file_name, encoding = "latin-1")
        f = open(file_name, "w+")
        temp_df.to_csv(f, lineterminator = "\n", encoding = "utf-8")
        f.close()

    def updater(self, new_DB: list):
        #OMS update
        ## OMS_Additional_UOM
        with open("config/OMS_DB/OMS_AdditionalUOM.csv", "a") as f:
            for line in new_DB[0]:
                writer_object = writer(f)
                writer_object.writerow(line)
                f.close()
        # temp_df = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")

        # with open("config/OMS_DB/OMS_AdditionalUOM.csv", "w+") as f:
        #     temp_df.to_csv(f, lineterminator = "\n")
        
        ## OMS_PaymentTerm
        with open("config/OMS_DB/OMS_PaymentTerm.csv") as f:
            for line in new_DB[1]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        # temp_df = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")

        # with open("config/OMS_DB/OMS_AdditionalUOM.csv", "w+") as f:
        #     temp_df.to_csv(f, lineterminator = "\n")

        ## OMS_InventoryList
        with open("config/OMS_DB/OMS_InventoryList.csv", "a") as f:
            for line in new_DB[2]:
                writer_object = writer(f)

                writer_object.writerow(line)
                f.close()
        # temp_df = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")

        # with open("config/OMS_DB/OMS_AdditionalUOM.csv", "w+") as f:
        #     temp_df.to_csv(f, lineterminator = "\n")

        ## OMS_UOM
        with open("config/OMS_DB/OMS_UOM.csv", "a") as f:
            df_uom = pd.read_csv("config/OMS_DB/OMS_UOM.csv")
            writer_object = writer(f)
            df = pd.read_csv("OMS_AdditionalUOM.csv")
            lis = df["AdditionalUnitsOfMeasureName"]

            temp_set = set(lis)

            for item in temp_set:
                if item not in list(df_uom["Name"]):
                    writer_object.writerow([item])
        # temp_df = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")

        # with open("config/OMS_DB/OMS_AdditionalUOM.csv", "w+") as f:
        #     temp_df.to_csv(f, lineterminator = "\n")

        #uom_sku udpate
        UOM = pd.read_csv("config/OMS_DB/OMS_AdditionalUOM.csv")
        uom = UOM[["BaseSKU", "AdditionalUnitsOfMeasureSKU", "NumberOfBaseUnitsInAdditionalUnit"]]
        keys = list(uom["BaseSKU"])

        dic = {}

        for i, key in enumerate(keys):
          dic.update({key: [uom["AdditionalUnitsOfMeasureSKU"][i], uom["NumberOfBaseUnitsInAdditionalUnit"][i]]})

        # self.elaborator("uom_sku.csv")

        df = pd.DataFrame(dic)
        df.to_csv("uom_sku.csv")