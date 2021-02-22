def get_XML_VALUES(i):
    import xml.etree.ElementTree as ET
    tree = ET.parse(i)
    rt = tree.getroot()
    BAID = (rt.get('BAId'))
    print(BAID)


def read_file_sftp(filepath,filename):
    import paramiko, os
    import sftp_config as con


    #remote_file=pathlib.Path( filename)
    #os.chdir(con.LOCAL_PATH)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=con.HOST, username=con.USERNAME, password=con.PASSWORD)
    remote_path = (con.XML_PATH + filepath)
    print(remote_path)
    sftp = ssh_client.open_sftp()
    sftp.chdir(remote_path)
    #data = sftp.listdir()

    #for i in data:
        #if i.startswith('SUM'):
            #with sftp.open(i) as f:
                #get_XML_VALUES(f)
    with sftp.open(filename) as f:
        get_XML_VALUES(f)

    f.close()
    sftp.close()
    ssh_client.close()
    return ()

def read_oracle():
    import cx_Oracle
    import oracle_config as config

    sql= f'Select  substr(replace(DR_DOCU_LINK_LINK,\'ENV\',\'ADDR\'),1,instr(replace(DR_DOCU_LINK_LINK,\'ENV\',\'ADDR\'),\'/\',-1) -1) filepath \
     , substr(replace(DR_DOCU_LINK_LINK,\'ENV\',\'ADDR\'),instr(replace(DR_DOCU_LINK_LINK,\'ENV\',\'ADDR\'),\'/\',-1) +1) filename from  DR_DOCUMENTS dr \
   where DR_ADDRESSEE_BA_PKEY=:BA \
   and DR_ASS_DOC_CR_DATE_TIMESTAMP = (select  max( DR_ASS_DOC_CR_DATE_TIMESTAMP) \
          from dr_documents where  DR_ADDRESSEE_BA_PKEY = dr.DR_ADDRESSEE_BA_PKEY)'
    print(sql)
    myfile=''
    try:
        # establish a new connection
        with cx_Oracle.connect(
                config.USERNAME,
                config.PASSWORD,
                config.dsn,
                encoding=config.encoding) as connection:
            # create a cursor

            with connection.cursor() as cursor:
                cursor.execute(sql,BA = 'BA0001034322')
                row = cursor.fetchone()
                if row:
                    myfilepath = row[0]
                    myfile=row[1]

    except cx_Oracle.Error as error:
        print(error)
    print(myfilepath,myfile)
    return (myfilepath,myfile)

def main():

    myfilepath,myfile = read_oracle()


if __name__ =="__main__":
    main()










