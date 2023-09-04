import pandas as pd
from csv import writer

class OMS_Creation:
  def __init__(self) -> None:
    self.uom = pd.read_csv("config/OMS_DB/OMS_UOM.csv")
    self.inventory = pd.read_csv("config/OMS_DB/OMS_InventoryList.csv")
    self.length = 0

  def UOM_Addition(self, input):
     for page in input:
      for product in page["Product*"][1:]:
          if product.split("-")[1] not in self.uom["Name"]:
              #Add uom to UOM
              #frontend input here
              lis_uom = [1]
              with open("config/OMS_DB/OMS_UOM.csv", "a") as f:
                 writer_object = writer(f)

                 writer_object.writerow(lis_uom)
                 f.close()
            
              pass
          
  def InventoryList_Addition(self, input):
     for page in input:
        self.length = len(page[list(page.keys())[0]])

        for product in page["Product*"][1:]:
           if product.split("-")[0] not in self.inventory["ProductCode"]:
              #Add production to Inventory_List
              #frontend input here
              lis_inventory = [i for i in range(122)]
              with open("config/OMS_DB/OMS_InventoryList.csv", "a") as f:
                 writer_object = writer(f)

                 writer_object.writerow(lis_inventory)
                 f.close()
            
              pass

  def OMS_generator(self, SalesImport):

    #OMS_UOM
    self.UOM_Addition(SalesImport)
    
    #OMS_InventoryList
    self.InventoryList_Addition(SalesImport)