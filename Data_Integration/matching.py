import json
import re
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
    def __init__(self) -> None:
        # parse_res: OCR parsed result for PO
        
        
        self.variables = {}
        self.data = []
        
        self.pair = {
            'PO Line #': "LINE",
            'Vendor Style': "VENDOR PN",
            'UPC/EAN': "UPC/GTIN",
            'Product/Item Description': "DESCRIPTIONLINE ITEM COMMENTS",
            "Dept #": "DESCRIPTIONLINE ITEM COMMENTS",
            'Unit Price': "UNIT COST/RETAIL PRICE",
            'Qty Ordered': "QTY",
            "Unit of Measure": "UOM",
        }
        
        self.initial_part = {
            "PO Line #": "",
            'Vendor Style': "",
            "UPC/EAN": "",
            "Product/Item Description": "",
            "Dept #": "",
            'Unit Price': "",
            'Qty Ordered': "",
            "Unit of Measure": "",
        }
        
        f = open("field_names.json")
        self.field_names = json.load(f)
        self.field_names_temp = []
        for item in self.field_names:
            self.field_names_temp.append(item) 
        for item in self.field_names_temp:
            a = list(self.pair.keys())
            if item in list(self.pair.keys()):
                (self.field_names).remove(item)
    
    def variable_init(self):
        self.variables = {}
        for key in self.field_names:
            self.variables[key] = ""
            
    def initial_part_init(self):
        self.initial_part = {}
        # self.initial_part = self.pair
        for key in self.pair:
            self.initial_part.update({key:""})
    
    def match_plain(self, input):
        res = []
            
        for i, _ in enumerate(input):
            pdf = input[f"PDF{i}"]
            
            for j, _ in enumerate(pdf):
                page = pdf[f"page{j}"]
                length = len(page)
                
                for item in page[1 : length - 1]:
                    res.append(item)
        
        for i in range(len(res)):
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
    
    def match_divide(self, input):
        input = list(input)
        input.remove("\n")
        input = "".join(input)
        input_ = input.split("Department Number")
        temp = []

        for i, element in enumerate(input_):
            if ":" in element: temp.append(i)

        f_th = input_[0:temp[1]]
        s_nd = input_[temp[1]:]
        
        return [" ".join(f_th), " ".join(s_nd)]
    
    def match_same(self, input):
        self.initial_part_init()
        
        for i, key in enumerate(self.initial_part):
            if key == "Product/Item Description":
                self.initial_part[key] = self.match_divide(input[self.pair[key]])[0]
                self.initial_part[key] = "".join(self.initial_part[key])
            
            elif key == "Dept #":
                self.initial_part[key] = "Department Number" + self.match_divide(input[self.pair[key]])[1]
                self.initial_part[key] = "".join(self.initial_part[key])
            elif key == 'Unit Price':
                self.initial_part[key] = re.findall(r'\d\.\d+', input[self.pair[key]])
                self.initial_part[key] = "".join(self.initial_part[key])
            elif key == 'Vendor Style':
                self.initial_part[key] = re.findall(r'\d', input[self.pair[key]])
                self.initial_part[key] = "".join(self.initial_part[key])
                
            else: self.initial_part[key] = input[self.pair[key]]
        
        return self.initial_part
    
    def match_formula(self, input):
        #return all {"field": field_value}
        for item in self.field_names:
            input.update({item: ""})
            
        return input
    
    def match_final(self, PO_res):
        # return final result
        output = self.match_plain(PO_res)
        
        for i, item in enumerate(output):
            item = self.match_same(item)
            item = self.match_formula(item)
            output.pop(i)
            output.insert(i, item)
        return output