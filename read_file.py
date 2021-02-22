import pandas as pd


def insert_oracle(df):

    from sqlalchemy import create_engine,types
    import os


    try :
        tns = """
          (DESCRIPTION =
            (ADDRESS = (PROTOCOL = TCP)(HOST = 10.30.110.15)(PORT = 1521))
            (CONNECT_DATA =
              (SERVER = DEDICATED)
              (SERVICE_NAME = CBIOPRD)
            )
          )
        """

        usr = "OPSUPP"
        pwd = "OKR"
        os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
        connection_string = f"{usr}:{pwd}@10.30.110.15:1521/CBIOPRD"
        #engine = create_engine(f'oracle://{connection_string}', encoding = 'utf-8' )
        import cx_Oracle
        engine = create_engine('oracle://%s:%s@%s' % (usr, pwd, tns), encoding = 'utf-8')

        #df.astype(str, copy=True, errors='raise')
        df['CO_LIMIT'] = df['CO_LIMIT'].astype(float)
        print(df.info())
        dtyp = {c:types.VARCHAR(df[c].str.len().max())
                for c in df.columns[df.dtypes =='object'].tolist()}

        from sqlalchemy.types import Integer, Text, String, DateTime
        df.to_sql('staff_data',engine,index=False, if_exists='replace',chunksize=1000,dtype=dtyp)
        #mycon.close()

    except :
        print("Error")
        raise


def read_file():
    #print(os.getcwd())
    #print(os.getcwd()

    df = pd.read_excel("staff_data.xlsx",encoding='utf-8',dtype='str' )

    #df.convert_dtypes(convert_integer=True)
    df.astype({"CO_LIMIT":'float'}).dtypes
    #print(df.info())
    return df

def main():
    df = read_file()
    insert_oracle(df)


main()