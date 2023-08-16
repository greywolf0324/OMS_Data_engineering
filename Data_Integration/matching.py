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
        
        self.initial_part = {
            "PO Line #": "",
            "Vendor Style": "",
            "UPC/EAN": "",
            "Product/Item Description": "",
            "Dept #": "",
            "Unit Price": "",
            "Qty Ordered": "",
            "Unit of Measure": "",
        }
        
        
    
    def variable_init(self):
        self.variables = {}
        for key in self.field_names:
            self.variables[key] = ""
            
    def initial_part_init(self):
        for key in self.initial_part:
            self.initial_part[key] = ""
    
    def match_plain(self, input):
        res = []
            
        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]
            
            for j, _ in enumerate(pdf):
                page = pdf[f"page{j}"]
                length = len(page)
                
                for item in page[1 : length - 1]:
                    res.append(item)
        
        for i in len(res):
            res[i] = {
                "LINE": res[i][0],
                "VENDOR PN": res[i][2],
                "UPC/GTIN": res[i][3],
                "DESCRIPTIONLINE ITEM COMMENTS": res[i][4],
                "UNIT COST/RETAIL PRICE": res[i][6],
                "QTY": res[i][7],
                "UOM": res[i][8],
                "ITEMTOTAL": res[i][9]
            }
        return res
    
    def match_same(self, input):
        self.initial_part_init()
        
        for key in self.initial_part:
            if key == "Product/Item Description":
                self.initial_part[key] = "fun"
            
            if key == "Dept #":
                self.initial_part[key] = "fun"
                
            else: self.initial_part[key] = input[self.pair[key]]
        
        return self.initial_part
    
    def match_formula(self, input):
        #return all {"field": field_value}
        
        return input
    
    def match_final(self, PO_res):
        # return final result
        input = self.match_plain(PO_res)
        
        for item in input:
            item = self.match_same(item)
            