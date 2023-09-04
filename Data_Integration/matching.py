import json
import re
import pandas as pd
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
        
        self.PO_keys = []
        self.variables = {}
        self.data = []
        self.length = 0
        self.pair = {
            'PO Line #': "LINE",
            'Vendor Style': "VENDOR PN",
            'UPC/EAN': "UPC/GTIN",
            'Product/Item Description': "DESCRIPTIONLINE ITEM COMMENTS",
            "Dept #": "DESCRIPTIONLINE ITEM COMMENTS",
            'Unit Price': "UNIT COST/RETAIL PRICE",
            'Qty Ordered': "QTY",
            "Unit of Measure": "UOM",
            "PO Date": "PO Date:",
            "Requested Delivery Date": "Requested Delivery Date:",
            "Ship Dates": "Requested Ship Date:",
            "Cancel Date": "Cancel Date:",
            "Vendor #": "Vendor #:",
            "Frt Terms": "Freight Terms:",
            "Payment Terms Disc Due Date": "Disc. Due Date:",
            "Payment Terms Disc Days Due": "Disc. Days:",
            "Payment Terms Net Due Date": "Net Due Date:",
            "Payment Terms Net Days": "Net Days:",
            "Buyers Catalog or Stock Keeping #": "SKU",
            "PO Total Amount": "total",
            "PO Total Weight": "Weight:",
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
            "PO Date": "",
            "Requested Delivery Date": "",
            "Ship Dates": "",
            "Cancel Date": "",
            "Vendor #": "",
            "Frt Terms": "",
            "Payment Terms Disc Due Date": "",
            "Payment Terms Disc Days Due": "",
            "Payment Terms Net Due Date": "",
            "Payment Terms Net Days": "",
            "Buyers Catalog or Stock Keeping #": "",
            "PO Total Amount": "",
            "PO Total Weight": "",
        }
        
        f = open("config/field_names_SalesImport_original.json")
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
                res.append(pdf[f"page{j}"])

        return res
    # def match_plain(self, input):
        # res = []
            
        # for i, _ in enumerate(input):
        #     pdf = input[f"PDF{i}"]
            
        #     for j, _ in enumerate(pdf):
        #         flag = 0
        #         page = pdf[f"page{j}"]
        #         length = len(page[0])
        #         print(length)
        #         for item in page[0][1 : length - 1]:
        #             if flag == 0:
        #                 flag = flag + 1
        #                 item.append(page[0][length - 1][9])
        #                 res.append(item)
                    
        #             else:
        #                 flag = flag + 1
        #                 item.append("")
        #                 res.append(item)

        # for i in range(len(input)):
        #     input[i] = {
        #         "LINE": input[i][0],
        #         "SKU": input[i][1],
        #         "VENDOR PN": input[i][2],
        #         "UPC/GTIN": input[i][3],
        #         "DESCRIPTIONLINE ITEM COMMENTS": input[i][4],
        #         "UNIT COST/RETAIL PRICE": input[i][6],
        #         "QTY": input[i][7],
        #         "UOM": input[i][8],
        #         "PO Date:": input[i][10],
        #         "Requested Delivery Date:": input[i][11],
        #         "Requested Ship Date:": input[i][12],
        #         "Cancel Date:": input[i][13],
        #         "Vendor #:": input[i][16],
        #         "Freight Terms:": input[i][18],
        #         "Disc. Due Date:": input[i][23],
        #         "Disc. Days:": input[i][24],
        #         "Net Due Date:": input[i][25],
        #         "Net Days:": input[i][26],
        #         "ITEMTOTAL": input[i][-1]
        #     }
        # return res
    
    def match_divide(self, input):

        input = list(input)
        input.remove("\n")
        input = "".join(input)
        input_ = input.split("Department Number")
        temp = []

        for i, element in enumerate(input_):
            if ":" in element: temp.append(i)

            # f_th = input_[0:temp[1]]
            # s_nd = input_[temp[1]:]
        return [input_[0:temp[1]], input_[temp[1]:]]
    
    def match_same(self, input):
        self.initial_part_init()
        
        length = len(input["LINE"])
        # for i, key in enumerate(self.initial_part):
        #     if key == "Product/Item Description":
        #         self.initial_part[key] = self.match_divide(input[self.pair[key]])[0]
        #         self.initial_part[key] = "".join(self.initial_part[key])
            
        #     elif key == "Dept #":
        #         self.initial_part[key] = "Department Number" + self.match_divide(input[self.pair[key]])[1]
        #         self.initial_part[key] = "".join(self.initial_part[key])
        #     elif key == 'Unit Price':
        #         self.initial_part[key] = re.findall(r'\d\.\d+', input[self.pair[key]])
        #         self.initial_part[key] = "".join(self.initial_part[key])
        #     elif key == 'Vendor Style':
        #         self.initial_part[key] = re.findall(r'\d', input[self.pair[key]])
        #         self.initial_part[key] = "".join(self.initial_part[key])
                
        #     else: self.initial_part[key] = input[self.pair[key]]
        
        # return self.initial_part

        for key in self.pair:
            if key == "Product/Item Description":
                input[key] = []
                input["Dept #"] = []

                for i in range(1, length):
                    input[key].append(self.match_divide(input[self.pair[key]][i])[0])
                    input["Dept #"].append(self.match_divide(input[self.pair[key]][i])[1])

                input[key].insert(0, "")
                input["Dept #"].insert(0, "")
                # print(input[key])
                # print(input["Dept #"])
                del input[self.pair[key]]
                
            elif key == "Dept #": continue
            
            elif key == "Unit Price":
                input[key] = []

                for i in range(1, length):
                    temp = re.findall(r'\d\.\d+', input[self.pair[key]][i])
                    input[key].append("".join(temp))
                
                input[key].insert(0, "")

                del input[self.pair[key]]
            
            elif key == 'Vendor Style':
                input[key] = []
                
                for i in range(1, length):
                    # print(input[self.pair[key]])
                    temp = re.findall(r'\d', input[self.pair[key]][i])
                    input[key].append("".join(temp))
                
                input[key].insert(0, "")
                del input[self.pair[key]]

            else:
                input[key] = input[self.pair[key]]
                del input[self.pair[key]]
        return input
    
    def match_formula(self, input):
        #return all {"field": field_value}
        temp_key = input.keys()

        for item in self.field_names:
            if item not in temp_key:
                temp = []
                
                for _ in range(self.length):
                    temp.append("")
                
                input.update({item: temp})
            
        return input
    
    def match_final(self, PO_res):


        # return final result
        output = self.match_plain(PO_res)
        
        # get PO_res keys
        self.PO_keys = list(output[0].keys())
        self.PO_inherited = []
        for key in self.pair:
            self.PO_inherited.append(self.pair[key])

        #register un-inherited keys
        
        # print(output[0])
        for page in output:
            self.length = len(page["LINE"])
            item = self.match_same(page)
            item = self.match_formula(item)
            # output.pop(i)
            # output.insert(i, item)
            for key in self.PO_keys:
                if key not in self.PO_inherited:
                    del item[key]
        
        df = pd.DataFrame(output[0])
        df.to_excel("sales_origin.xlsx")

        return output
        