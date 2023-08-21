from OCR.parse import PDF_parsing
from Data_Integration.matching import PO_Match
from Integration_Add.Integrator import Integreate_All
from Generation.generator import OMS_Generator
from csv import DictWriter
import json
import pandas as pd
import csv

def main():
    paths = ["E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\sample.pdf"]
    # OCR
    print("On PDF parsing...")
    parser = PDF_parsing()
    PO_res = parser.PO_parser(paths)

    # Data_Integration
    print("On Match Operating...")
    matcher = PO_Match()
    matching_res = matcher.match_final(PO_res)

    
    # Integration_Add
    print("Integrating...")
    integreator = Integreate_All()
    sales_import = integreator.Integrate_final(matching_res)
    
    # Generating OMS
    print("Generating OMS...")
    generator = OMS_Generator()
    OMS = generator.generator_all(sales_import)
    
    print("Just a second, writing...")
    f = open("SalesImport_fieldnames.json")
    field_names = json.load(f)

    with open('Exam/output/output.csv', 'w') as outfile:
        writer = DictWriter(outfile, field_names)
        writer.writeheader()
        writer.writerows(sales_import)
    # with open("output.json", 'w') as f:
    #     json.dump(sales_import, f)
    print("successful!")
if __name__ =="__main__":
    
    main()
    
    