from OCR.parse import PDF_parsing
from Data_Integration.matching import PO_Match
from Integration_Add.Integrator import Integreate_All

def main():
    paths = ["E:\work\Daily\8_10\_N\dataflow\input(PO)\PDF\sample.pdf"]

    # OCR
    parser = PDF_parsing()
    PO_res = parser.PO_parser(paths)

    # Data_Integration
    matcher = PO_Match()
    matching_res = matcher.match_formula(PO_res)

    # Integration_Add
    integreator = Integreate_All.Integrate_All()
    sales_import = integreator(matching_res)
    
if __name__ =="__main__":
    
    main()
    
    