from OCR.parse import PDF_parsing

parser = PDF_parsing()

paths = ["E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\sample.pdf"]
res = parser.PO_parser(paths)

