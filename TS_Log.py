from TS_Parameters import *
from datetime import datetime
def print_log(message):
    '''
    Depending on the current state of the running the code (tsp_print_logs=True/False (Run))
    the message would be printed on console (tsp_print_logs==True)
    And the message will be written in the log file regardless of tsp_print_logs value
    :param message:
    :return:
    '''
    if tsp_print_logs:
        print(message)

    Log_(message)

def Log_(message):
    '''
    Writing the input message in the log file.
    :param message:
    :return:
    '''
    tsp_log_file = tsp_log_folder + 'LOG-'+ str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day) + '.log'

    with open(tsp_log_file, "a") as logger:
        logger.write(str(datetime.today())+": "+str(message)+"\n")
        logger.close()




