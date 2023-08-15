import pdfplumber

class PDF_parsing():
    def __init__(self) -> None:
        pass
    
    def PO_parser(self, paths):
        #this function will generate PO table
        
        res = {}
        
        for i, path in enumerate(paths):
            res[f"PDF{i}"] = {}
            pdf = pdfplumber.open(path)
            
            for page_num, page in enumerate(pdf.pages):
            # page = pdf.pages[1]
                res[f"PDF{i}"][f"page{page_num}"] = []
                for ele in page.extract_table():
                    res[f"PDF{i}"][f"page{page_num}"].append(ele)
        
        return res