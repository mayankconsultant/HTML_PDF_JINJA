INPUT_PATH=r'C:\Users\MayankPC\PycharmProjects\XML_FILES_TO_CSV\XML_INPUT\CSV_FILES'

INPUT_QUERY=r"Select  DOC_REFNUM , substr(bi_reference, 1, instr ( bi_reference,'/',-1) )  BI_REFERENCE from  BGH_BILL_IMAGE_REF b " \
"where  cust_id = custid "  \
"and bi_date = (select  max(bi_date) from BGH_BILL_IMAGE_REF where cust_id = b.cust_id)" \
            " and bi_date>sysdate-10"


INSERT_QUERRY="INSERT INTO BGH_BILL_IMAGE_REF " \
              "Select DOC_ID , '" + str ('CS') + "' || DOC_REFNUM ,BA_ID,BA_CODE,CUST_ID,CUSTNUM,CONTR_ID,CONTR_CODE,DOC_GEN_DATE,"\
"BILL_MODE,BILL_TYPE,BILL_CYCLE,BI_MEDIUM_SHDES,BI_REFERENCE_TYPE, replace( BI_REFERENCE,'INV','CSINV')  BI_REFERENCE,BI_DATE,BI_TYPE from BGH_BILL_IMAGE_REF b "\
"where  cust_id = custid and bi_date = (select  max(bi_date) from BGH_BILL_IMAGE_REF where cust_id = b.cust_id) "

UPDATE_QUERRY="UPDATE BGH_BILL_IMAGE_REF SET BI_REFERENCE=replace( BI_REFERENCE,'INV','CSINV')  where  DOC_REFNUM = 'drefnum' "

PAY_QUERRY=r"Select sum(PAY) from (select  case when "