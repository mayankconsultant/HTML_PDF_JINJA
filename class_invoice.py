import pandas as pd
import os
import xml.etree.ElementTree as ET
import logging


class Invoice:
    logger = logging.getLogger(__name__)

    def get_all_dataframes(self ):
        tree = ET.parse(self.filename)
        rt = tree.getroot()
        Cust_df = pd.DataFrame(columns=['CUSTCODE', 'CO_CODE', 'MSISDN', 'USAGE', 'RENTAL', 'FEES', 'TOTAL'])
        for tag in rt.iter('CustRef'):
            self.custid = tag.get('Id')

            for ch in tag.findall('./Charge'):
                if ch.get('Id') == "936":
                    fee = float(ch.get('Amount'))
            if fee > 0:
                amount = float(0)
                for sub_ch in tag.findall('./SumItem'):

                    for ch in sub_ch.findall('./Charge'):
                        # if co_id == "CONTR0000169304":
                        #   print(service + " " + call_type + "-"+ ch.get("Id") )
                        if ch.get("Id") in ("98", "99"):
                            Amount = float(Amount) + float(ch.get('Amount'))
                            # if co_id == "CONTR0000169304":
                            # print("I Love U")
                    for ch in sub_ch.findall('./Txt'):
                        occ_text = str(ch.text)
                        Fees_df = get_co_fees_df(Fees_df, custcode, '-', occ_text, Amount)
                    Cust_df = get_cust_df(Cust_df, custcode, 'NA', 'NA', float(0), float(0), float(fee))



    def __init__(self,filename, custcode):
        self.filename = filename
        self.custcode = custcode
        self



def main():
    pass

if __name__=="__main__":
    main()
