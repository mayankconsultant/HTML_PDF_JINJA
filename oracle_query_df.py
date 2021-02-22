from sqlalchemy import create_engine as eng
import pandas as pd
import cx_Oracle
import oracle_config as oc


def read_data2():
    dsn_tns = cx_Oracle.makedsn(oc.HOST, oc.PORT, oc.SERVICE_NAME)

   # conn = cx_Oracle.connect(oc.USERNAME,oc.PASSWORD, dsn_tns)
    sql = "select  * from customer_all  where  rownum < 20000"
    #df = pd.read_sql(sql, con=conn)
    #print(df)

    with cx_Oracle.connect(
            oc.USERNAME,
            oc.PASSWORD,
            oc.dsn,
            encoding=oc.encoding) as connection:
        df=pd.read_sql(sql,connection)

    print(df)

def read_data () :
    connstr = "oracle://{}:{}@{}".format(oc.USERNAME, oc.PASSWORD, oc.HOST +":" + oc.PORT + "/"+oc.SERVICE_NAME  )
    print(connstr)
    conn = eng(connstr)
    sql="select  plcode, shdes, PLMNNAME from MPDPLTAB"
    df= pd.read_sql(sql,con=conn)
    print(len(df))

def main ():
    read_data2()

if __name__ =="__main__":
    main()