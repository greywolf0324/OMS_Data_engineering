import pandas as pd

class NOTICER:
  def __init__(self) -> None:
    self.additional_uom = pd.read_csv("config/uom_sku.csv")
    self.paymentterms = pd.read_csv("config/OMS_DB/OMS_PaymentTerm.csv")
    self.length = 0
    self.new_additional_uom = set()
    self.new_paymentterm = set()
    self.new_InventoryList = set()

  def getter(self, matching_res):
    for i, element in enumerate(matching_res):
      self.length = len(element[list(element.keys())[0]])

      for k in range(1, self.length):
        print(element["Vendor Style"][k])
        if (element["Vendor Style"][k] not in self.additional_uom.keys()) and (element["Vendor Style"][k] not in self.new_additional_uom):
          self.new_additional_uom.add(element["Vendor Style"][k])
      
      if element["Frt Terms"][0] == "":
        self.new_paymentterm.add(element["Frt Terms"][0])
      
      else:
        if element["Frt Terms"][0] not in list(self.paymentterms["Name"]):
          print(element["Frt Terms"])
          self.new_paymentterm.add(element["Frt Terms"][0])
    
    self.new_InventoryList = self.new_additional_uom

    return [self.new_additional_uom, self.new_paymentterm, self.new_InventoryList]