from jinja2 import Environment , FileSystemLoader

  # Select DR_ASS_DOC_NUMBER_EXTERNAL_ID,
  # DR_ASS_DOC_RF_DATE_TIMESTAMP + DR_ASS_DOC_RF_DATE_TIME_OFFSET/86400 INV_DATE ,
  # trunc( ( DR_ASS_DOC_RF_DATE_TIMESTAMP + DR_ASS_DOC_RF_DATE_TIME_OFFSET/86400  ) - 1/(60*24) ) END_DATE,
  #  Trunc ( (DR_ASS_LAST_SEND_DATE_TIMEST + DR_ASS_LAST_SEND_DATE_TIME_OFF/86400) + 1/(24*60) )  START_DATE,
  #  trunc( last_day( DR_ASS_DOC_RF_DATE_TIMESTAMP + DR_ASS_DOC_RF_DATE_TIME_OFFSET/86400  ) + 1 )  DUE_DATE ,
  #  '$WORK/DOC'||DR_DOCU_LINK_LINK
  #   from  DR_DOCUMENTS dr
  # where DR_ADDRESSEE_BA_PKEY='BA0001034322'-- DR_ADDRESSEE_CUSTOMER_ID = 964809
  # and DR_ASS_DOC_CR_DATE_TIMESTAMP = (select  max( DR_ASS_DOC_CR_DATE_TIMESTAMP) from dr_documents where  DR_ADDRESSEE_BA_PKEY = dr.DR_ADDRESSEE_BA_PKEY)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("with_float.html")

template_vars = {"custcode" :"2.17",     #ADDRESS
                 "custname" : "UNMISS PABX",  #ADDRESS
                 "invoice_dt" :"04-Apr-2020",                   #INVOICE DATE TYPE = INV
                 "line1": "C-6,601, AL Nasar Complex,Africa Road",  #ADDRESS LINE2 +LINE3
                 "line2":" Near Afra, Sudan",                       #ADDRESS LINE4 + LINE 5
                 "country":"Sudan", #ADDRESS COUNTRY
                 "msisdn": "211987548682",              #ADDRESS MSISDN
                 "email":"finance_dept@yahoo.com",      #ADDRESS EMAIL
                 "invoice_no":"REG0000045789",             #DB
                 "invoice_st_dt":"01-Mar-2020",
                 "invoice_end_dt":"31-Mar-2020",
                 "invoice_due_dt":"01-May-2020",
                 "invoice_dt":"01-Apr-2020",
                 "custcare_no":"21191239123",
                 "custcare_email":"zain_custcare@ss.zain.com",
                 "voice_sms_other_home":255.1256,
                 "voice_sms_other_roaming":10.2564,
                 "gprs_home":125.25,
                 "gprs_roaming":0,
                 "rentals":50,
                 "subscription":0,
                 "fees":2.1568,
                 "total":550.24586,
                 "tax":"0.00",
                 "prev_balance":1400,
                 "payments":-400,
                 "curr_due":1550.24586
    }

breakup_labels=["voice_sms_other_home","voice_sms_other_roaming","gprs_home","gprs_roaming","rentals","subscription","fees"]
breakup_values=[255.1256,10.2564,125.25,0,50,0,2.1568]
colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]
import matplotlib.pyplot as plt
import numpy as np

#plt.pie(breakup_values,labels=breakup_labels,colors=colors,autopct='%1.1f%%',)
x=np.arange(len(breakup_labels))
plt.bar( x,breakup_values)
plt.xlabel('breakup', fontsize=5)
plt.xticks(x, breakup_labels, fontsize=5, rotation=30)
plt.tight_layout()
plt.savefig('usage.png', bbox_inches = "tight")

html_out =template.render(template_vars)

filename="Invoice_float.html"

with open(filename,"w+") as f:
    print(html_out)
    f.write(html_out)
    f.close()

import webbrowser

webbrowser.open(filename)

import pdfkit
options = {
        'page-size': 'A4',
        'margin-top': '0in',
        'layout' : 'letter',
        'margin-bottom': '0in',
        'encoding': 'UTF-8',
        'disable_smart_shrinking': 'False',
        'footer_right': "Page [page] of [toPage]",

               }

pdfkit.from_file(filename, filename.split(".")[0] + ".pdf")