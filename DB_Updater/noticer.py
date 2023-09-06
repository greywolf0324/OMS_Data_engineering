import pandas as pd

class NOTICER:
  def __init__(self) -> None:
    self.additional_uom = pd.read_csv("config/uom_sku.csv")
    self.length = 0
    self.new_additional_uom = []
    self.new_paymentterm = []
    self.new_InventoryList = []

  def getter(self, matching_res):
    for i, element in enumerate(matching_res):
      self.length = len(element[list(element.keys())[0]])

      for k in range(1, self.length):
        if element["Vendor Style"][k] not in self.additional_uom.keys():
          self.new_additional_uom.append(element["Vendor Style"][k])
      
      if element["Frt Terms"] == "":
        self.new_paymentterm.append(element["Frt Terms"])
      
      else:
        if element["Frt Terms"] not in list(self.paymentterms["Name"]):
          self.new_paymentterm.append(element["Frt Terms"])
    
    self.new_InventoryList = self.new_additional_uom

    return [self.new_additional_uom, self.new_paymentterm, self.new_InventoryList]