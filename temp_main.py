import pandas as pd
from OCR.parse import PDF_parsing
import pdfplumber
from csv import DictWriter


path = "E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\sample.pdf"
pdf = pdfplumber.open(path)

parser = PDF_parsing()

res = parser.PO_parser([path])
ress = []

for key_d in res.keys():
    for key_p in res[key_d].keys():
        ress.append(res[key_d][key_p])

df = pd.DataFrame(columns=ress[0][0])

i = 0
for content in ress:
    for k, row in enumerate(content):
        if k == 0: continue
        else:
            df.loc[i] = row
            i = i + 1

df.to_csv("put.csv")
    
# with open('put.csv', 'w') as outfile:
#     writer = DictWriter(outfile, ress[0][0])
#     writer.writeheader()
#     writer.writerows(res)
    


# parser = PDF_parsing()

# res = parser.PO_parser(["E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\multi.pdf"])

# # import csv

# # with open("out.txt", "w", newline="") as f:
# #     writer = csv.writer(f)
# #     for i in range(len(res["PDF0"])):
# #         writer.writerows(res['PDF0'][f"page{i}"])
        
# print(res["PDF0"]["page0"][1][4])


# def check_bboxes(word, table_bbox):
#         #Check whether word is inside a table bbox.
#         l = word['x0'], word['top'], word['x1'], word['bottom']
#         r = table_bbox
        
#         return l[0] > r[0] and l[1] > r[1] and l[2] < r[2] and l[3] < r[3]

# path = "E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\sample.pdf"
# pdf = pdfplumber.open(path)

# for page in pdf.pages:

#     tables = page.find_tables
    
#     print(tables, type(tables))
    
#     table_bboxes = [i.bbox for i in tables]
#     tables = [{'table': i.extract(), 'doctop': i.bbox[1]} for i in tables]
#     non_table_words = [word for word in page.extract_words() if not any(
#         [check_bboxes(word, table_bbox) for table_bbox in table_bboxes])]
#     lines = []
#     for cluster in pdfplumber.utils.cluster_objects(non_table_words+tables, 'doctop', tolerance=5):
#         if 'text' in cluster[0]:
#             lines.append(' '.join([i['text'] for i in cluster]))
#         elif 'table' in cluster[0]:
#             lines.append(cluster[0]['table'])
            
# print(lines)