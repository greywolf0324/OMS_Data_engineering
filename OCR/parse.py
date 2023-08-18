import pdfplumber
import re

class PDF_parsing:
    def __init__(self) -> None:
        pass
    
    def re_fun(self, str_input: str) -> dict:
        if str_input == None:
            return None
        loc = str_input.rfind(":")
        left, right = str_input[:loc] + str_input[loc], (str_input[loc:])[1:]
        
        return {left: right}
    
    def PO_parser(self, paths: list):
        #this function will generate PO table
        
        res = {}
        
        for k, path in enumerate(paths):
            res[f"PDF{k}"] = {}
            pdf = pdfplumber.open(path)
            
            for page_num, page in enumerate(pdf.pages):
            # page = pdf.pages[1]
                res[f"PDF{k}"][f"page{page_num}"] = []
                cols_add = []
                for i, ele in enumerate(page.extract_tables()):
                    if i != 2:
                        items = [item for sublist in ele for item in sublist]
                        for item in items: 
                            if self.re_fun(item) == None:
                                continue
                            else:
                                cols_add.append(self.re_fun(item))
                print(cols_add)
                table_main = page.extract_tables()[2]
                
                for i, item in enumerate(table_main):
                    print("#",i)
                    for dic in cols_add:
                        if i == 0: item.append(list(dic.keys())[0])
                        elif i == 1: item.append(list(dic.values())[0].replace("\n", ""))
                        else: item.append("")
                    print(item)
                print(type(table_main))
                res[f"PDF{k}"][f"page{page_num}"].append(table_main)
        
        return res