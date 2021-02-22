import smtplib
import logging
import datetime
import os


def get_logger(
        LOG_FORMAT='%(asctime)s %(funcName)s %(levelname)-8s %(message)s',
        LOG_NAME='',
        LOG_FILE_INFO='file.log',
        LOG_FILE_ERROR='file.err'):
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # comment this to suppress console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    # stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='a+')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='a+')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log


def send_mail():
    user = "mayank.shah@ss.zain.com"
    password = "Zain@1727"

    msg = """From: From Person <mayank.shah@ss.zain.com>
To: Mayank H Shah <maaluv81@gmail.com>
MIME-Version: 1.0
Content-type: text/html
Subject: SMTP HTML e-mail test 2 

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
<p> So this is done now Finally </p>
"""

    try:
        smtpObj = smtplib.SMTP(host='172.16.101.13', port=2526)
        smtpObj.sendmail(user, 'maaluv81@gmail.com', msg)
        mylogger.info("DOne")
    except Exception as e:
        mylogger.error(e)




def main():
    mytime = str(datetime.datetime.now().strftime("_%d%B%Y%H%M%S"))

    if not os.path.exists(os.path.join(os.path.curdir,'LOGS','SENDMAIL')): os.makedirs(os.path.join(os.path.curdir,'LOGS','SENDMAIL'))


    global mylogger

    mylogger = get_logger(LOG_FILE_INFO="LOGS/SENDMAIL/lg_" + mytime + ".log",
                          LOG_FILE_ERROR="LOGS/SENDMAIL/er_" + mytime + ".err")


    send_mail()


if __name__=="__main__":
    main()