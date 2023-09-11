from OCR.parse import Buc_parsing, PEPCO_Parsing
from Data_Integration.matching import PO_Match
from DB_Updater.noticer import NOTICER
from DB_Updater.DB_Updater import Udpater
from Integration_Add.Integrator import Integrate_All
from OMS_Creation.oms import OMS_Creation
from csv import DictWriter
import json
import pandas as pd
import csv
from openpyxl import load_workbook
import xlsxwriter
import os

def Sys_Buc():
    paths = [r"E:\work\Daily\8_10\_N\OMS_Data_engineering\Experiment_result\input\PDF\Buc-EE's\multi.pdf"]
    
    # OCR : Parsing PDF and generate table results
    print("On PDF parsing...")
    parser = Buc_parsing()
    PO_res = parser.PO_parser(paths)

    # Data_Integration: Generate SalesImport_Original
    print("On Match Operating...")
    matcher = PO_Match()
    matching_res = matcher.match_final(PO_res)

    # # Notation: Add following Info to DB
    print("Getting newal things...")
    noticer = NOTICER()
    addition = noticer.getter(matching_res)
    print(addition)
    #get response from frontend based on "addition"
    response_from_frontend = [] #{"OMS_AdditionalUOM": "OMS_PaymentTerm": "OMS_InventoryList":}
    # ########################################################################################
    # ##    Add "addition" info to OMS_AdditionalUOM, OMS_PaymentTerm, OMS_InventoryList    ##
    # ########################################################################################
    # print("DB Updating...")
    # udpater = Udpater()
    # udpater.updater(response_from_frontend)

    # Integration_Add : Generate [SalesImport, new_sku, new_paymentterm]
    print("Integrating...")
    integreator = Integrate_All()
    SalesImport = integreator.Integrate_final(matching_res)
    
    # # Generating OMS
    # print("Generating OMS...")
    # generator = OMS_Creation()
    # generator.OMS_generator(SalesImport)
    
    print("Just a second, writing...")
    f = open("config/fieldnames_SalesImport.json")

    field_names = json.load(f)

    # generate excel output file
    if os.path.isfile("SalesImport.xlsx"):
        os.remove("SalesImport.xlsx")
    book = xlsxwriter.Workbook("SalesImport.xlsx")
    sheet = book.add_worksheet("cont_excel")
    keys = list(SalesImport[0].keys())
    for idx, header in enumerate(field_names):
        sheet.write(0, idx, header)

    book.close()

    book = load_workbook("SalesImport.xlsx")
    sheet = book.get_sheet_by_name("cont_excel")
    
    for dic in SalesImport:
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
    
    book.save(filename = "SalesImport.xlsx")

    print("successful!")

def Sys_PEPCO():
    paths = [r"E:\work\Daily\8_10\_N\OMS_Data_engineering\Experiment_result\input\PDF\PEPCO\ORD00913820_01 _ CK BRANDS LIMITED _ 264252_orderSupp.pdf"]
    # OCR : Parsing PDF and generate table results
    print("On PDF parsing...")
    parser = PEPCO_Parsing()
    PO_res = parser.PO_parser(paths)

if __name__ == "__main__":
    
    st = "Sys_Buc"
    
    globals()[st]()
    
    