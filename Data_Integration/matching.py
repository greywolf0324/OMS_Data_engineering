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
# ITEMTOTAL: PO Total Amount


class PO_Match:
    def __init__(self, parse_res) -> None:
        # parse_res: OCR parsed result for PO
        f = open("field_names.json")
        self.field_names = json.load(f)
        
        self.parse_res = parse_res
        
        self.variables = {}
        self.data = []
        
        self.pair = {
            "PO Line #": "LINE",
            "Vendor Style": "VENDOR PN",
            "UPC/EAN": "UPC/GTIN",
            "Product/Item Description": "DESCRIPTIONLINE ITEM COMMENTS",
            "Dept #": "DESCRIPTIONLINE ITEM COMMENTS",
            "Unit Price": "UNIT COST/RETAIL PRICE",
            "Qty Ordered": "QTY",
            "Unit of Measure": "UOM",
        }
        
        for i, _ in enumerate(self.parse_res):
            pdf = self.parse_res[f"PDF{i}"]
            for j, _ in enumerate(pdf):
                page = pdf[f"page{j}"]
                length = len(page)
                data = page[1 : length - 1]
    
    def variable_init(self):
        self.variables = {}
        for field in self.field_names:
            self.variables[field] = ""
    
    def match_same(self, input):
        self.variable_init()
        
        for key in self.pair:
            self.variables[key] = input[self.pair[key]]
        
        return self.variables
    
    def match_formula(self, input):
        #return all {"field": field_value}
        
        return [{}]