from OCR.parse import PDF_parsing
from Data_Integration.matching import PO_Match
from Integration_Add.Integrator import Integreate_All
from Generation.generator import OMS_Generator
from csv import DictWriter
import json
import pandas as pd
import csv
from openpyxl import load_workbook
import xlsxwriter
import os

def main():
    paths = [r"E:\work\Daily\8_10\_N\OMS_Data_engineering\Exam\input\PDF\multi.pdf"]
    # OCR : Parsing PDF and generate table results
    print("On PDF parsing...")
    parser = PDF_parsing()
    PO_res = parser.PO_parser(paths)

    # Data_Integration : Generate SalesImport_Original
    print("On Match Operating...")
    matcher = PO_Match()
    matching_res = matcher.match_final(PO_res)

    # Integration_Add : Generate SalesImport
    print("Integrating...")
    integreator = Integreate_All()
    sales_import = integreator.Integrate_final(matching_res)
    print(sales_import)
    # # Generating OMS

    # print("Generating OMS...")
    # generator = OMS_Generator()
    # OMS = generator.generator_all(sales_import)
    
    print("Just a second, writing...")
    f = open("config/fieldnames_SalesImport.json")
    field_names = json.load(f)
    print(type(field_names))
    # with open('Exam/output/output.csv', 'w') as outfile:
    #     writer = DictWriter(outfile, field_names)
    #     writer.writeheader()
    #     writer.writerows(sales_import)


    # with open("output.json", 'w') as f:
    #     json.dump(sales_import, f)

    # generate excel output file
    if os.path.isfile("output.xlsx"):
        os.remove("output.xlsx")
    book = xlsxwriter.Workbook("output.xlsx")
    sheet = book.add_worksheet("cont_excel")
    keys = list(sales_import[0].keys())
    for idx, header in enumerate(field_names):
        sheet.write(0, idx, header)

    book.close()

    book = load_workbook("output.xlsx")
    sheet = book.get_sheet_by_name("cont_excel")
    
    for dic in sales_import:
        for i in range(len(dic[keys[0]])):
            temp = []

            for key in field_names:
                # print(len(res[dic][di]["LINE"]))
                # print(res[dic][di])
                # print(key)
                if key in keys:
                    temp.append(dic[key][i])
                else:
                    temp.append("")
            sheet.append(temp) 
    
    book.save(filename = "output.xlsx")

    print("successful!")
if __name__ == "__main__":
    
    main()
    
    