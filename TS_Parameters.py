# print whatever is logged

tsp_print_logs = True
# Server type for addressing the encoders and log file on the disk
tsp_server_type ='remote' #'remote'#'local' # remote

if tsp_server_type=='local':
    tsp_log_folder = '/Users/kazemqazanfari/Documents/Agnes/IE_LOG/'

elif tsp_server_type=='remote':
    tsp_log_folder = '/home/ubuntu/IE_LOG/'


RapidApi_key = '71368470-6135-11e9-b08e-592da48838e4'
