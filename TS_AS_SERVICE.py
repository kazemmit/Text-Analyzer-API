from flask import Flask, request
from flask import Response
from flask_restful import Resource, Api
import ast
import sys
import traceback
from bson import json_util
from TS_Log import print_log
from TS_Universal_Sentence_Encoder import read_USE_model,init_USE
from TS_Error_Codes import *
from TS import TextSimilarity,CheckRequestSource,read_topics,TopicsSimilarity
from TS_Sentiment import Text_Sentiment

topics,topics_preprocessed = read_topics()
print_log("Loading USE encoder......")
try:
    #Universal_Encoder = read_USE_model()
    USE_ENCODER = 0
    session, embedded_text, text_input = init_USE()
    topics_model = session.run(embedded_text, feed_dict={text_input: topics_preprocessed})

    print_log("USE encoder has been loaded successfully!")
except:
    print_log("USE encoder has NOT been loaded successfully!")
    in_ = input('Would you like to continue without having USE encoder loaded (y/n)?')
    if in_.strip() != 'y' and in_.strip() != 'Y':
        exit()

print_log("Waiting for commands...")

app = Flask(__name__)
@app.route("/similarityscore", methods=["POST"])
def post_1():
    #request_data = request.data
    # print('////////')
    # print( request.form.get('first sentence'))
    # print(request.form.get('second sentence'))
    # print(str(request.get_data()))
    # print('********')
    # print(str(request))
    # print('@@@@@@@@')
    #print(request_data)

    #request_ = request_data #request_data

    #request_ = ast.literal_eval(ast.literal_eval(str(request_)[1:].replace('null','None').replace('true','True').replace('false','False')))
    #request_ = ast.literal_eval(ast.literal_eval(str(request_)))

    # print('*********Request*********')
    # print(request_)
    # print('*****End of request******')

    # CheckParam_res = CheckParam(request_)
    # print_log(CheckParam_res)
    #
    # if CheckParam_res==tse_err_param:
    #     return json_util.dumps({'result': CheckParam_res})

    #USE_ENCODER = read_USE_model()

    if True:#CheckRequestSource(request):

        try:
            data_ =  json_util.dumps({'result': TextSimilarity('relatedness',# request_['similarity type']
                                                             request.form.get('first_text'),
                                                             request.form.get('second_text'),
                                                             USE_ENCODER,session,embedded_text,text_input) })
        except Exception:
            try:
                exc_info = sys.exc_info()
            finally:
                formatted_lines = traceback.format_exc()
                print_log(formatted_lines)
                data_ =  json_util.dumps({'result': tse_err0})

    else:

        data_ = json_util.dumps({'result': tse_err_invalid_request_source})

    resp = Response(data_, status=200, mimetype='application/json')
    return resp


@app.route("/sentimentanalysis", methods=["POST"])
def post_2():

    if CheckRequestSource(request):

        try:
            data_ =  json_util.dumps({'result':Text_Sentiment(
                                                             request.form.get('text'))  })
        except Exception:
            try:
                exc_info = sys.exc_info()
            finally:
                formatted_lines = traceback.format_exc()
                print_log(formatted_lines)
                data_ =  json_util.dumps({'result': tse_err0})
    else:

        data_ = json_util.dumps({'result': tse_err_invalid_request_source})

    resp = Response(data_, status=200, mimetype='application/json')
    return resp


@app.route("/topictagging", methods=["POST"])
def post_3():

    if CheckRequestSource(request):

        try:
            data_ =  json_util.dumps({'result': TopicsSimilarity('relatedness',topics_model,topics,# request_['similarity type']
                                                             request.form.get('text'),
                                                             USE_ENCODER,session,embedded_text,text_input) })
        except Exception:
            try:
                exc_info = sys.exc_info()
            finally:
                formatted_lines = traceback.format_exc()
                print_log(formatted_lines)
                data_ =  json_util.dumps({'result': tse_err0})

    else:

        data_ = json_util.dumps({'result': tse_err_invalid_request_source})

    resp = Response(data_, status=200, mimetype='application/json')
    return resp


@app.route('/', methods=['GET'])
def home():
    if True:#CheckRequestSource(request):
        return "<h1>Anis Text Analyzer API is working!</h1><p>This api includes some popular text analytics tools, such as word and sentence similarity, sentiment analysis, and text classification.</p>"
    else:
        data_ =  json_util.dumps({'result':tse_err_invalid_request_source})
        resp = Response(data_, status=200, mimetype='application/json')
        return resp



print_log("Server is running!")
api = Api(app)
app.run(host='0.0.0.0',port=5002)







