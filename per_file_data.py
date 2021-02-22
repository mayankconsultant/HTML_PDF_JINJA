import  pandas as pd
import  os
import logging
import xml.etree.ElementTree as ET
import datetime
from jinja2 import Environment , FileSystemLoader
import cx_Oracle
import oracle_config as config
import CONF as c

LOGING_LEVEL="DEBUG"
logging.basicConfig(filename="perfile_data_trial.log",level=LOGING_LEVEL,filemode="w",format='%(asctime)s-%(funcName)s -%(levelname)s - %(message)s')
# GET_BILLS_CUSTCODE=['2.17','2.18','3.326']
# GET_BILLS_CUSTCODE=[ '2.30','3.455']
GET_BILLS_CUSTCODE=['2.18','3.326']
# GET_BILLS_CUSTCODE=[ '3.170','3.198']
# GET_BILLS_CUSTCODE=[ '2.30']
rounding_factor = 5

template_vars={}

def update_pdfname(docref):
    try:
        # establish a new connection
        sql = c.UPDATE_QUERRY.replace('drefnum', str(docref))
        logging.debug(sql)
        with cx_Oracle.connect(
                config.USERNAME,
                config.PASSWORD,
                config.dsn,
                encoding=config.encoding) as connection:
            # create a cursor

            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                print( 'UPDATE DONE So: ' )




    except cx_Oracle.Error as e:
        logging.error('ORACLE : get_filename error' + str(e))
        raise
    except Exception as e:
        logging.error('SQL: Error in execute sql :' + str(e.args))
        raise

    return

def get_pdfname(cust_id):
    try:
        # establish a new connection

        sql=c.INPUT_QUERY.replace('custid', str(cust_id))
        logging.debug(sql)
        with cx_Oracle.connect(
                config.USERNAME,
                config.PASSWORD,
                config.dsn,
                encoding=config.encoding) as connection:
            # create a cursor

            with connection.cursor() as cursor:
                cursor.execute(sql )

                row = cursor.fetchone()
                if row is None:
                    logging.warning(' No rows Found in Dr_documents for customer skipping UPDATE' + str(cust_id))
                    pdfname = 'trial'
                    bi_ref='None'
                if row:
                    pdfname =  str(row[0])
                    bi_ref=row[1]
                    logging.debug(pdfname)



    except cx_Oracle.Error as e:
        logging.error('ORACLE : get_filename error' + str(e))
        raise
    except Exception as e:
        logging.error('SQL: Error in execute sql :' + str(e.args))
        raise

    return pdfname, bi_ref


def create_pdf(template_vars,filename):
    try:
        dd=format(datetime.datetime.now(),'%b')
        if not os.path.exists(os.path.join(os.path.curdir,dd)): os.makedirs(os.path.join(os.path.curdir,dd))
        outfile_path= os.path.join(os.path.curdir,dd)
        folder_name = os.path.join(outfile_path, filename.replace(' ', '_'))
        if not os.path.exists(folder_name) : os.makedirs(folder_name)
        filename,bi_refname = get_pdfname(template_vars['cust_id'])
        create_html(template_vars, folder_name, str('CSINV') + filename)

    except Exception as e:
        logging.error(e.args)
        raise


    try:

        import pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '0.15in',
            'margin-right': '0in',
            'margin-bottom': '0.15in',
            'margin-left': '0.15in',
            'encoding': 'UTF-8',
            'no-outline': None,
        }
        pdfkit.from_file('CSINV' + str(filename) + ".html", os.path.join(folder_name, 'CSINV' + str(filename)) + '-L-C0.pdf', options=options)
    except Exception as e:
        logging.error(e.args)
        raise

    try :
        update_pdfname(filename)
        print('cp -p /CBiO/bscs/bscsadm/WORK/ZSS/MAYANK/XMLTEST/'+dd.upper() + str('2021') +'/REAL/CSINV'+ str(filename)+ '-L-C0.pdf ' + str(bi_refname) + ".")
    except Exception as e:
        logging.error(e.args)
        raise

def create_html(template_vars,folder_name,filename):
    logging.info(" Creating HTML ")
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("with_float.html")
    html_out = template.render(template_vars)

    filename = filename + ".html"

    with open(filename, "w+") as f:
        # print(html_out)
        f.write(html_out)
        f.close()

    import webbrowser

    webbrowser.open(filename)
    print(str(template_vars['cust_id']) +str( '-->' ) + str (filename) + ".pdf" )


def append_total_row(df):
    df_sum_row = pd.DataFrame(df.sum(axis=0,numeric_only=True)).T
    df_sum_row = df_sum_row.reindex(columns=df.columns)
    df_sum_row.iloc[-1, 0] = 'TOTAL'
    df_sum_row = df_sum_row.fillna(value="-")
    df = df.append(df_sum_row, ignore_index=True)

    return df




def get_dn_num(v_contract):
    for i in v_contract.findall("./DN"):
        dn_num = i.get('Num')

    return dn_num

def get_co_usage_df(df,v_co,v_dn,v_home_voice,v_home_sms ,v_home_gprs ,v_home_Usage_others ,v_roaming_gprs , v_roaming_others , v_roaming_sms ,v_roaming_voice,v_usage):
    co_us_dict={'CO_CODE':v_co,'MSISDN':v_dn,'VOICE(H)':float(v_home_voice), 'SMS(H)':float(v_home_sms) , \
                'GPRS(H)':float(v_home_gprs) ,'OTHERS(H)':float(v_home_Usage_others) ,'VOICE(V)':float(v_roaming_voice) , 'SMS(V)':float(v_roaming_sms), \
                'OTHERS(V)':float(v_roaming_others),'TOTAL':float(v_usage) }
    tmp_df = pd.DataFrame(data=[co_us_dict], columns=co_us_dict.keys())
    df = df.append(tmp_df,ignore_index=True)
    return df

def get_co_roaming_df (v_roaming_df,v_co,v_dn,visting_plcode,v_roaming_gprs, v_roaming_others, v_roaming_sms, v_roaming_voice, roaming ):
    logging.debug('roaing df' +  str (v_roaming_voice ))
    try:
        co_us_dict={'CO_CODE':v_co,'MSISDN':v_dn,'VOICE(V)':float(v_roaming_voice) , 'SMS(V)':float(v_roaming_sms), \
                'OTHERS(V)':float(v_roaming_others),'TOTAL':float(roaming) }
        tmp_df = pd.DataFrame(data=[co_us_dict], columns=co_us_dict.keys())
        df = v_roaming_df.append(tmp_df,ignore_index=True)
    except Exception as e:
        logging.error(format="%m", )
    return df

def get_co_usage(Contracts,co_code,v_dn_num, v_usage_df, v_roaming_df):
    usage =0
    roaming = 0
    visting_plcode=""
    home_voice = home_sms = home_gprs = home_Usage_others = roaming_gprs = roaming_others = roaming_sms = roaming_voice = 0
    for pc in Contracts.findall("PerCTInfo"):

        if pc.get('CT') == "U":

            for ch in pc.findall('./Charge'):
                if ch.get('Id') == "838":

                    usage = round(float(ch.get('Amount')),rounding_factor)
                if ch.get('Id') == "938":

                    usage = round(float(usage) + float(ch.get('Amount')),rounding_factor)

            if usage > 0 :
                roaming=0
                for sub_ch in pc.findall('./SumItem'):

                    article = list(sub_ch.get('ArticleString').split("."))
                    service, call_type = article[3], article[6]
                    if call_type!='F': visting_plcode=article[8]
                    for ch in sub_ch.findall('./Charge'):
                        if service == "6" and call_type == "F" and ch.get("Id") in ("98", "99"):
                            home_voice = round(home_voice + float(ch.get('Amount')) ,rounding_factor)
                        elif call_type != 'F' and service == "6" and ch.get("Id") in ("98", "99"):
                            roaming_voice = round ( roaming_voice + float(ch.get('Amount')), 5)
                            roaming = round( roaming +roaming_voice,rounding_factor)
                        elif service == "7" and call_type == 'F' and ch.get("Id") in ("98", "99"):
                            home_sms = round( home_sms + float(ch.get('Amount')) ,rounding_factor)
                        elif call_type != 'F' and service == "7" and ch.get("Id") in ("98", "99"):
                            roaming_sms = roaming_sms + float(ch.get('Amount'))
                            roaming = round ( roaming + roaming_sms, 5)
                        elif service == "13" and call_type == 'F' and ch.get("Id") in ("98", "99"):
                            home_gprs = round ( home_gprs + float(ch.get('Amount')),rounding_factor)
                        elif call_type != 'F' and service == "13" and ch.get("Id") in ("98", "99"):
                            roaming_gprs = round( roaming_gprs + float(ch.get('Amount')) ,rounding_factor)
                            roaming = round (roaming + roaming_gprs,rounding_factor)
                        elif call_type != 'F' and ch.get("Id") in ("98", "99"):
                            roaming_others = round (roaming_others + float(ch.get('Amount')) ,rounding_factor)
                            roaming = round (roaming + roaming_others ,rounding_factor)
                        elif call_type == 'F' and ch.get("Id") in ("98", "99"):
                            home_Usage_others = round (home_Usage_others + float(ch.get('Amount')),rounding_factor)
                v_usage_df = get_co_usage_df(v_usage_df, co_code, v_dn_num, home_voice, home_sms, home_gprs, home_Usage_others, \
                                roaming_gprs, roaming_others, roaming_sms, roaming_voice, usage)
                if roaming > 0:
                    v_roaming_df=get_co_roaming_df(v_roaming_df,co_code,v_dn_num,visting_plcode,roaming_gprs, roaming_others, roaming_sms, roaming_voice, roaming )

    return usage,v_usage_df,v_roaming_df

def get_co_rental_df(df,v_co,v_dn,v_tel,v_gprs,v_silver_offer,v_rental_others,v_rental):
    co_rnt_dict={'CO_CODE':v_co,'MSISDN':v_dn,'TEL':float(v_tel),'GPRS':float(v_gprs),
                 'SILVER_OFFER':float(v_silver_offer),
                'OTHERS':float(v_rental_others),'TOTAL':v_rental }
    tmp_df = pd.DataFrame(data=[co_rnt_dict], columns=co_rnt_dict.keys())
    df = df.append(tmp_df,ignore_index=True)
    return df



def get_co_rental(Contracts,co_code,v_dn_num, v_rental_df):
    rental =0
    tel_rent= 0
    gprs_rent=0
    others_rent = 0
    Silver_offer = 0
    for pc in Contracts.findall("PerCTInfo"):

        if pc.get('CT') == "A":

            for ch in pc.findall('./Charge'):
                if ch.get('Id') == "838":

                    rental = round(float(ch.get('Amount')),rounding_factor)
                if ch.get('Id') == "938":

                    rental = round(float(rental) + float(ch.get('Amount')),rounding_factor)

            if rental > 0 :
                for sub_ch in pc.findall('./SumItem'):

                    article = list(sub_ch.get('ArticleString').split("."))
                    service = article[3]
                    for ch in sub_ch.findall('./Charge'):
                        if service == "6" and ch.get("Id") in ("98", "99"):
                            tel_rent = round (tel_rent + float(ch.get('Amount')),rounding_factor)
                        elif service == "13" and ch.get("Id") in ("98", "99"):
                            gprs_rent = round (gprs_rent + float(ch.get('Amount')),rounding_factor)
                        elif service == "169" and ch.get("Id") in ("98", "99"):
                            Silver_offer = round (Silver_offer + float(ch.get('Amount')),rounding_factor)
                        elif ch.get("Id") in ("98", "99"):
                            others_rent = round (others_rent + float(ch.get('Amount')),rounding_factor)
                v_rental_df = get_co_rental_df(v_rental_df, co_code, v_dn_num, tel_rent,gprs_rent,Silver_offer,others_rent, rental)


    return rental,v_rental_df



def get_co_fees_df(v_fees_df, co_code, v_dn_num, txt_val,v_fee):
    co_rnt_dict={'CUSTCODE_OR_CO_CODE':str(co_code),'MSISDN':str(v_dn_num),'OCC_TEXT':txt_val,'OCC_AMOUNT':float(v_fee)
                 }
    tmp_df = pd.DataFrame(data=[co_rnt_dict], columns=co_rnt_dict.keys())
    v_fees_df = v_fees_df.append(tmp_df,ignore_index=True)
    return v_fees_df


def get_co_fees(Contracts,co_code,v_dn_num, v_fees_df):
    fees =float(0)
    occ_text=""
    amount=float(0)
    if v_dn_num not in ('-','0',0, ""):

        for pc in Contracts.findall("PerCTInfo"):

            if pc.get('CT') == "O":

                for ch in pc.findall('./Charge'):
                    if ch.get('Id') == "838":

                        fees = round(float(ch.get('Amount')),rounding_factor)
                    if ch.get('Id') == "938":

                        fees = round(float(fees) + float(ch.get('Amount')),rounding_factor)

            if fees > 0 :
                for sub_ch in pc.findall('./SumItem'):

                    for ch in sub_ch.findall('./Charge'):

                        if  ch.get("Id") in ("98", "99"):
                            amount = round(float(amount) + float(ch.get('Amount')),rounding_factor)

                    for ch in sub_ch.findall('./Txt'):
                        occ_text=ch.text

                        v_fees_df = get_co_fees_df(v_fees_df, co_code, v_dn_num, occ_text,amount)


    return fees,v_fees_df



def get_cust_df(df,v_cust,v_co,v_dn,v_us,v_ren,v_fees):
    logging.debug('cust_df level')
    cust_dict={'CUSTCODE':v_cust,'CO_CODE':v_co,'MSISDN':v_dn,'USAGE':float(v_us),'RENTAL':float(v_ren),'FEES':float(v_fees),'TOTAL':round(float(v_us)+float(v_ren)+float(v_fees),rounding_factor )  }
    logging.debug('TOTAL' + str (round(float(v_us)+float(v_ren)+float(v_fees),rounding_factor)))

    tmp_df = pd.DataFrame(data=[cust_dict], columns=cust_dict.keys())

    tmp_df['TOTAL'] = tmp_df['TOTAL'].apply(lambda x: '{:.2f}'.format(x))
    tmp_df['TOTAL'] =tmp_df['TOTAL'].astype('float')
    # print(tmp_df['TOTAL'].dtype)
    #tmp_df['TOTAL']=tmp_df['TOTAL'].round(decimals=rounding_factor)
    df = df.append(tmp_df,ignore_index=True)
    return df



def get_all_dataframes(xmlfile):
    try:
        tree = ET.parse(xmlfile)
        rt = tree.getroot()
    except Exception as e:
        logging.error(' Error in Get_all_DF: ' + str(e.args))
        raise e
    ba_id = rt.get("Id")[0:4] + "_" + rt.get("BAId")
    cust_df = pd.DataFrame(columns=['CUSTCODE','CO_CODE','MSISDN','USAGE','RENTAL','FEES','TOTAL'])
    usage_df=pd.DataFrame(columns=['CO_CODE','MSISDN','VOICE(H)', 'SMS(H)','GPRS(H)','OTHERS(H)', \
                                   'VOICE(V)', 'SMS(V)','OTHERS(V)','TOTAL'])
    roaming_df=pd.DataFrame(columns=['VOICE(V)', 'SMS(V)','OTHERS(V)','TOTAL'])
    rental_df=pd.DataFrame(columns=['CO_CODE','MSISDN','TEL','GPRS','SILVER_OFFER','OTHERS','TOTAL'])

    fees_df=pd.DataFrame(columns=['CUSTCODE_OR_CO_CODE','MSISDN','OCC_TEXT','OCC_AMOUNT'])

    cnt = 0
    occ_amt =0
    occ_text=""
    for tag in rt.iter('CustRef'):
        custid = tag.get('Id')
        custcode = str(tag.get('CustCode'))
        logging.debug('CUSTID :' + str(custid) + ' ; CUSTCODE :' + str(custcode))
        for ch in tag.findall('./Charge'):
            if ch.get('Id') == "936":
                occ_amt = round(float(ch.get('Amount')),rounding_factor)
        if occ_amt > 0 :
            amount=float(0)
            for sub_ch in tag.findall('./SumItem'):
                for ch in sub_ch.findall('./Charge'):
                    if ch.get("Id") in ("98", "99"):
                        amount = round(float(amount) + float(ch.get('Amount')),rounding_factor)

                for ch in sub_ch.findall('./Txt'):
                    occ_text = str(ch.text)
                    fees_df = get_co_fees_df(fees_df, custcode, '-', occ_text, amount)
                cust_df = get_cust_df(cust_df, custcode, 'NA', 'NA', float(0), float(0), float(occ_amt))
        for Contracts in tag.findall("./Contract"):

                dn_num = str(get_dn_num(Contracts))
                coid=str(Contracts.get('Id'))

                co_usage,usage_df,roaming_df=get_co_usage(Contracts,coid,dn_num,usage_df,roaming_df)
                co_rent, rental_df = get_co_rental(Contracts, coid, dn_num, rental_df)
                co_fee, fees_df = get_co_fees(Contracts, coid, dn_num, fees_df)
                cnt = cnt + 1





                cust_df= get_cust_df(cust_df,custcode,coid,dn_num,co_usage,co_rent,co_fee)

    return ba_id,cust_df,usage_df, rental_df,fees_df,roaming_df

def get_filename(customer, template_vars):


        sql = f' Select  filepath, filename,DR_ASS_DOC_NUMBER_EXTERNAL_ID INV_NO, \
                     m.INV_DATE  Inv_date, \
                    m.Start_date START_DATE, \
                     m.End_date  END_DATE, \
                    m.DUE_DATE  Due_date ,' \
              f'    nvl ( (Select sum(DECODE (m.currency,  \'USD\', cachkamt_pay,  \'SSP\', CACHKAMT_GL)) from cashreceipts_all \
                where  customer_id = m.DR_ADDRESSEE_CUSTOMER_ID \
                and catype  not in ( 10,12) \
                 and to_char ( trunc ( CAENTDATE), \'dd-mon-yyyy\') >= to_date( m.Start_date , \'dd-MON-yyyy\') \
                 and to_char ( trunc ( CAENTDATE), \'dd-mon-yyyy\') <  to_date( m.INV_DATE  , \'dd-MON-yyyy\') \
                 ), 0) PAyment \
                , m.currency, m.custname,m.line1,m.line2,country,m.email,m.msisdn, m.prev_balance,m.cust_id \
                 from ( \
                            SELECT DR_ADDRESSEE_CUSTOMER_ID , SUBSTR ( \
                                                                REPLACE (DR_DOCU_LINK_LINK, \'ENV\', \'ADDR\'), 1,\
                                                    INSTR (REPLACE (DR_DOCU_LINK_LINK, \'ENV\', \'ADDR\'), \'/\', -1) - 1)  filepath, \
                            SUBSTR (REPLACE (DR_DOCU_LINK_LINK, \'ENV\', \'SUM\'), \
                                        INSTR (REPLACE (DR_DOCU_LINK_LINK, \'ENV\', \'SUM\'), \'/\', -1) + 1)   filename, \
                                DR_ASS_DOC_NUMBER_EXTERNAL_ID,    TO_CHAR ( \
                                DR_ASS_DOC_RF_DATE_TIMESTAMP      + DR_ASS_DOC_RF_DATE_TIME_OFFSET / 86400,        \'dd-MON-yyyy\') \
          INV_DATE,\
       TO_CHAR (  TRUNC (  (  DR_ASS_DOC_RF_DATE_TIMESTAMP + DR_ASS_DOC_RF_DATE_TIME_OFFSET / 86400)  - 1 / (60 * 24)),\'dd-MON-yyyy\') END_DATE,\
       TO_CHAR (TRUNC ((  DR_ASS_LAST_SEND_DATE_TIMEST+ DR_ASS_LAST_SEND_DATE_TIME_OFF / 86400)+ 1 / (24 * 60)),\'dd-MON-yyyy\') START_DATE,\
       TO_CHAR (TRUNC (LAST_DAY (DR_ASS_DOC_RF_DATE_TIMESTAMP + DR_ASS_DOC_RF_DATE_TIME_OFFSET / 86400) + 1),\'dd-MON-yyyy\') DUE_DATE,\
         (SELECT DECODE (currency,  \'19\', \'USD\',  \'44\', \'SSP\',  currency)   FROM customer_all\
         WHERE customer_id = DR_ADDRESSEE_CUSTOMER_ID)   currency,  UPPER (NVL (CCLINE2, CCLINE3)) custname,  ' \
              f'UPPER (NVL (CCLINE4, \'None\')) LINE1, \
       UPPER (CCLINE5) Line2, \
       UPPER (CCLINE6) country, \
       LOWER (ccemail) email, \
       CCSMSNO msisdn, \
       (SELECT PREV_BALANCE FROM may_postpaid_contr_01 WHERE customer_id = DR_ADDRESSEE_CUSTOMER_ID) PREV_BALANCE,' \
              f'CUSTOMER_ID CUST_ID \
  FROM DR_DOCUMENTS dr, CContact_all ca WHERE     ' \
              f'DR_ADDRESSEE_CUSTOMER_ID = (SELECT customer_id   FROM customer_all WHERE custcode = :BA) \
       AND dr.DR_ADDRESSEE_CUSTOMER_ID = ca.customer_id \
       AND CCBILL = \'X\' \
       AND DR_ASS_DOC_CR_DATE_TIMESTAMP =(SELECT MAX (DR_ASS_DOC_CR_DATE_TIMESTAMP) FROM dr_documents WHERE ' \
              f' DR_ADDRESSEE_BA_PKEY = dr.DR_ADDRESSEE_BA_PKEY)) m '
        logging.debug(sql)
        template_vars['myfile'] = ''
        try:
            # establish a new connection
            with cx_Oracle.connect(
                    config.USERNAME,
                    config.PASSWORD,
                    config.dsn,
                    encoding=config.encoding) as connection:
                # create a cursor

                with connection.cursor() as cursor:
                    cursor.execute(sql, BA=customer,)
                    row = cursor.fetchone()
                    if row is None :
                        logging.warning(' No rows Found in Dr_documents for customer ' + str(customer))
                    if row:
                        myfilepath = row[0]
                        template_vars['custcode'] = customer
                        template_vars['myfile'] = row[1]
                        template_vars['invoice_no']=row[2]
                        template_vars['invoice_dt']=str(row[3])
                        template_vars['invoice_st_dt']=row[4]
                        template_vars['invoice_end_dt']=row[5]
                        template_vars['invoice_due_dt']=row[6]
                        template_vars['payment'] = row[7]
                        template_vars['currency']=row[8]
                        template_vars['custname']=row[9]
                        template_vars['line1'] = row[10]
                        template_vars['line2'] =row[11]
                        template_vars['country'] = row[12]
                        template_vars['email'] = row[13]
                        template_vars['msisdn'] = row[14]
                        template_vars['prev_balance']= row[15]
                        template_vars['cust_id'] = row[16]
                        logging.info(template_vars
                                 )


        except cx_Oracle.Error as e:
            logging.error('get_filename error' + str(e))
            raise
        except Exception as e:
            logging.error(' Error in execute sql :' + str(e.args))
            raise



        return  template_vars

def main():
        import datetime

        try :

            v_start_time = datetime.datetime.now()
            logging.info("Starting to  log:" + " " + str(v_start_time) )
            mypath = r"C:\Users\MayankPC\PycharmProjects\XML_FILES_TO_CSV\XML_INPUT"
            for customer in GET_BILLS_CUSTCODE:
                template_vars = {}
                start_time = datetime.datetime.now()
                logging.info("Customer to start :" + str( customer) + " " +str(start_time) )
                template_vars = get_filename(customer,template_vars)
                logging.debug('filestr :' + str (template_vars['myfile']))
                file_found=False
                if template_vars['myfile'] !="":
                    for files in os.listdir(mypath):
                        if files.startswith(template_vars['myfile']) :
                            file_found = True

                            logging.info("Opened file: " + files)
                            baid, cust_df, usage_df, rental_df, fees_df,roaming_df = get_all_dataframes(os.path.join(mypath,files))
                            logging.debug("baid:" + str(baid) + " voice_sms_other_home : " + str((usage_df['VOICE(H)'].sum() +usage_df['SMS(H)'].sum() + usage_df['OTHERS(H)'].sum() )  ) )
                            template_vars['custcare_no'] ='21191239123'
                            template_vars['custcare_email']='coporatesales@ss.zain.com'
                            template_vars['voice_sms_other_home'] =\
                                round(usage_df['VOICE(H)'].sum() + usage_df['SMS(H)'].sum() + usage_df['OTHERS(H)'].sum(),rounding_factor)
                            template_vars['gprs_home']=round(usage_df['GPRS(H)'].sum(),rounding_factor)
                            template_vars['voice_sms_other_roaming'] =\
                                round (usage_df['VOICE(V)'].sum() + usage_df['SMS(V)'].sum() + usage_df['OTHERS(V)'].sum(),rounding_factor)
                            template_vars['rentals']=round (rental_df['TOTAL'].sum(),rounding_factor)
                            #template_vars['gprs_roaming'] = usage_df['GPRS(V)'].sum()
                            template_vars['fees']=round(fees_df['OCC_AMOUNT'].sum(),rounding_factor)
                            template_vars['subscription']=0
                            template_vars['taxes'] =0
                            template_vars['total']=round(template_vars['voice_sms_other_home'] +\
                                                      template_vars['gprs_home'] + \
                                                      template_vars['voice_sms_other_roaming'] + \
                                                      template_vars['rentals'] + \
                                                      template_vars['fees'], rounding_factor)
                            template_vars['curr_due']=round(template_vars['total'] +
                                                            template_vars['prev_balance'] -  template_vars['payment'],rounding_factor)
                            logging.info("Raoming Df :" + str ( roaming_df.count() ))
                            cust_df = append_total_row(cust_df)
                            usage_df = append_total_row(usage_df)
                            rental_df = append_total_row(rental_df)
                            fees_df = append_total_row(fees_df)
                            roaming_df=append_total_row(roaming_df)

                            template_vars['cust_table']=cust_df.to_html(classes='mystyle',index=True,sparsify=True,table_id = "cust_table")
                            template_vars['usage_table'] = usage_df.to_html(classes='mystyle', index=True, sparsify=True,
                                                                          table_id="usage_table")
                            template_vars['rental_table'] = rental_df.to_html(classes='mystyle', index=True, sparsify=True,
                                                                          table_id="rental_table")
                            template_vars['occ_table'] = fees_df.to_html(classes='mystyle', index=True, sparsify=True,
                                                                          table_id="occ_table")
                            #logging.debug("Final TEM_VAR:" + str(template_vars))



                            #create_html(template_vars,"Test_file")

                            create_pdf(template_vars,str(template_vars['custname'] + "_" + str(template_vars['invoice_dt'].replace("-","_")  )) )
                            #    logging.debug("logginglevel :" + str (logging.Logger.level))

                    if not file_found: logging.warning("No File Found for :" + str(customer) + " filename : " + str(  template_vars['myfile'] )  )
                end_time = datetime.datetime.now()
                logging.info("Customer ended :" + str(customer) + " in " + str(  end_time -start_time )  )
        except Exception as e:
                    logging.error(' Error 3 :' + str(e ))
                    raise

        finally:
            logging.info("Program Ends in " + str(datetime.datetime.now() - v_start_time))

if __name__=="__main__":
    main()