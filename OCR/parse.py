import pdfplumber
import re
import pandas as pd
from openpyxl import load_workbook
import xlsxwriter
import os

class PDF_parsing:
    def __init__(self) -> None:
        self.keys = ['LINE', 'SKU', 'VENDOR PN', 'UPC/GTIN', 'DESCRIPTIONLINE ITEM COMMENTS', 'MARKS AND\nNUMBERS', 'UNIT COST/RETAIL\nPRICE', 'QTY', 'UOM', 'ITEMTOTAL', 'PO Date:', 'Requested Delivery Date:', 'Requested Ship Date:', 'Cancel Date:', 'Delivery Window:', 'Shipping Window:', 'Vendor #:', 'Department #:', 'Freight Terms:', 'Preferred Carrier:', 'Terms Type', 'Terms Basis:', 'Terms Disc\n%:', 'Disc. Due Date:', 'Disc. Days:', 'Net Due Date:', 'Net Days:', 'Description:', 'TYPE', 'SERVICE TYPE', 'PERCENT', 'RATE', 'QTY_', 'UOM_', 'DESCRIPTION', 'AMOUNT', 'Total Qty:', 'Weight:', 'Volume:', 'Purchase Order Total:', '280.80']


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
            
            # for page_num, page in enumerate(pdf.pages):
            # # page = pdf.pages[1]
            #     res[f"PDF{k}"][f"page{page_num}"] = []
            #     cols_add = []
            #     for i, ele in enumerate(page.extract_tables()):
            #         if i != 2:
            #             items = [item for sublist in ele for item in sublist]
            #             for item in items: 
            #                 if self.re_fun(item) == None:
            #                     continue
            #                 else:
            #                     cols_add.append(self.re_fun(item))
            #     table_main = page.extract_tables()[2]
                
            #     for i, item in enumerate(table_main):
            #         # print("#",i)
            #         for dic in cols_add:
            #             if i == 0: item.append(list(dic.keys())[0])
            #             elif i == 1: item.append(list(dic.values())[0].replace("\n", ""))
            #             else: item.append("")
            #     res[f"PDF{k}"][f"page{page_num}"].append(table_main)

            for page_num, page in enumerate(pdf.pages):
                res[f"PDF{k}"][f"page{page_num}"] = {}

                for key in self.keys:
                    res[f"PDF{k}"][f"page{page_num}"].update({key: []})
                
                #non main table addition
                non_product_tables = []

                for i, table in enumerate(page.extract_tables()):
                    if i == 2:
                        product_table = table
                    if i != 2:
                        items = [item for sublist in table for item in sublist]
                        for item in items: 
                            if self.re_fun(item) == None:
                                continue
                            else:
                                non_product_tables.append(self.re_fun(item))

                non_product_dic = {}
                for dic in non_product_tables:
                    non_product_dic.update(dic)
                
                non_blank_keys = list(non_product_dic.keys())

                for key in self.keys:
                    if key == "UOM_":
                        res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic["UOM"])
                    elif key == "QTY_":
                        res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic["QTY"])
                    else:
                        if key in non_blank_keys:
                            res[f"PDF{k}"][f"page{page_num}"][key].append(non_product_dic[key])
                        else:
                            res[f"PDF{k}"][f"page{page_num}"][key].append("")

                # main table addition
                product_keys = product_table[0]
                product_table_ = product_table[1 : len(product_table) - 1]
                
                product_dic = {}

                for key in product_keys:
                    product_dic.update({key:[]})

                for line in product_table_:
                    product_dic['LINE'].append(line[0])
                    product_dic['SKU'].append(line[1])
                    product_dic['VENDOR PN'].append(line[2])
                    product_dic['UPC/GTIN'].append(line[3])
                    product_dic['DESCRIPTIONLINE ITEM COMMENTS'].append(line[4])
                    product_dic['MARKS AND\nNUMBERS'].append(line[5])
                    product_dic['UNIT COST/RETAIL\nPRICE'].append(line[6])
                    product_dic['QTY'].append(line[7])
                    product_dic['UOM'].append(line[8])
                    product_dic['ITEMTOTAL'].append(line[9])
                
                for i in range(len(product_table_)):
                    for key in self.keys:
                        if key in product_keys:
                            res[f"PDF{k}"][f"page{page_num}"][key].append(product_dic[key][i])
                        else:
                            res[f"PDF{k}"][f"page{page_num}"][key].append("")
                temp_total = [product_table[len(product_table) - 1][9]]
                for _ in range(len(product_table) - 2):
                    temp_total.append("")
                res[f"PDF{k}"][f"page{page_num}"].update({"total": temp_total})
                # for key in res[f"PDF{k}"][f"page{page_num}"]:
                #     print(key, "\t", len(res[f"PDF{k}"][f"page{page_num}"][key]))
                
                # print(res[f"PDF{k}"][f"page{page_num}"])

        if os.path.isfile("temp.xlsx"):
            os.remove("temp.xlsx")
        book = xlsxwriter.Workbook("temp.xlsx")
        sheet = book.add_worksheet("cont_excel")
        for idx, header in enumerate(self.keys):
            sheet.write(0, idx, header)
        sheet.write(0, len(self.keys), "total")
        book.close()

        book = load_workbook("temp.xlsx")
        sheet = book.get_sheet_by_name("cont_excel")
        for dic in res:
            for di in res[dic]:
                for i in range(len(res[dic][di]["LINE"])):
                    temp = []

                    for key in res[dic][di].keys():
                        # print(len(res[dic][di]["LINE"]))
                        # print(res[dic][di])
                        # print(key)
                        temp.append(res[dic][di][key][i])
                    sheet.append(temp)


        book.save(filename = "temp.xlsx")
        temp = []
        
        print(temp)
        # pd.DataFrame(data = temp).to_excel("temp.xlsx", index = False)
        return res