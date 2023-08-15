import json

# LINE: PO Line #
# SKU: (not yet)
# VENDOR PN: Vendor Style
# UPC/GTIN: UPC/EAN
# DESCRIPTIONLINE ITEM COMMENTS: Product/Item Description, Dept #
# MARKS AND NUMBERS: (not yet)
# UNIT COST/RETAIL PRICE: Unit Price
# QTY: Qty Ordered
# UOM: Unit of Measure
# ITEMTOTAL: 


class PO_Match:
    def __init__(self, parse_res) -> None:
        # parse_res: OCR parsed result for PO
        f = open("field_names.json")
        self.parse_res = parse_res
        self.field_names = json.load(f)
        self.variables = {}
        
        for field in self.field_names:
            self.variables[field] = 0
        
    def match_same(self):
        self.variables[""]