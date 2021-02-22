import  pandas as pd
import CONF
import os
import matplotlib.pyplot as plt

def read_dir():
    mypath = CONF.INPUT_PATH
    return (mypath+'\data_un_0303_test.csv')

def Learn_pic(df):
    fig, ax = plt.subplots()
    plt.tight_layout()
    #mm = df.TEL_RENT.value_counts()
    # print(mm.index)
    #mm.plot(kind='bar', )
    # df.TEL_RENT.value_counts().plot(kind='bar', position=1)
    # df.GPRS_RENT.value_counts().plot(kind='bar',color='k',position =0,)
    # plt.savefig('TEL_RENT.png', bbox_inches="tight" )
    print( df.GPRS_RENT.value_counts())
    graph_df = df['TEL_RENT'].value_counts().rename('TEL_RENT').to_frame().con(df['GPRS_RENT'].value_counts().rename('GPRS_RENT').to_frame())
    #graph_df=pd.merge(df['TEL_RENT'].value_counts(),df['GPRS_RENT'].value_counts(),left_on=None,right_on=None,how='outer')
    #graph_df.plot(kind='bar',)
    df.plot(subplots=True,kind='bar' )
    plt.savefig('TEL_RENT.png', bbox_inches="tight" )

def read_df():
    # FILENAME, CUSTNUM, CUSTCODE, CO_CODE, DN_NUM, USAGE, FEES, RENTAL, SUBSCRIPTION, TEL_RENT, GPRS_RENT

    ff = read_dir()
    df=pd.read_csv(ff)#,dtype={'TEL_RENT':float,'GPRS_RENT':float})
    # print(df.head(1))
    #print(df['TEL_RENT'].value_counts())
    # print( df[ (df.GPRS_RENT=='0.0') & (df.TEL_RENT=='0.0')] )
    # print (df.describe())
    # print(pd.__version__)
    # df['TEL_RENT'].astype('float')
    #df['TEL_RENT']=pd.to_numeric(df['TEL_RENT'])
    # for c in df['TEL_RENT'] :
    #     print(c + ' : ' + str(type(c)))
    # # df['TEL_RENT'].apply(lambda x:float(x) )
    # print (df.dtypes)
    #print(df[(df.TEL_RENT=='TEL_RENT')])
    print(df.shape)
    df= df.drop(6048,axis=0)
    df.TEL_RENT=df.TEL_RENT.astype('float')
    df.GPRS_RENT=df.GPRS_RENT.astype('float')
    print(df.TEL_RENT.dtype)
    Learn_pic(df)


def main():
    read_df()

if __name__=='__main__':
    main()