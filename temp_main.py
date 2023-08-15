from OCR.parse import PDF_parsing

parser = PDF_parsing()

res = parser.PO_parser(["E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\multi.pdf"])

import csv

with open("out.txt", "w", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(res["PDF0"])):
        writer.writerows(res['PDF0'][f"page{i}"])