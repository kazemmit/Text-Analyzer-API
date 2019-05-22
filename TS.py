from scipy import spatial
from TS_Error_Codes import *
from TS_Log import print_log
from TS_Universal_Sentence_Encoder import generate_models_use
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
import string
from TS_Parameters import RapidApi_key

def VectorSimilarity(first_vec,second_vec):
    '''
    Calculating the cosine similarity between two vectors
    :param first_vec:
    :param second_vec:
    :return: a number between 0-1 (the higher, the more similar)
    '''
    if sum(first_vec)==0 or sum(second_vec)==0:
        return 0
    try:
        return  (2-spatial.distance.cosine(first_vec,second_vec))/2
    except:
        print_log(tse_err_sim_calculation)
        return 0

def text_pre_process(text,remove_stopword = True,toLower = True,remove_punctuations_numbers=True,min_word_len=3):
    text = text.replace('\n', ' ').replace('\t', ' ')

    if toLower:
        text = text.lower()

    if remove_punctuations_numbers:
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
        text = text.translate(translator)
        text = ''.join(e for e in text if e.isalpha() or e in ' ')

    if remove_stopword:
        words = [i.strip() for i in text.split(' ') if (i not in stop) and (len(i) >= min_word_len)]
    else:
        words = [i.strip() for i in text.split(' ') if len(i) >= min_word_len]

    return {'sentence':' '.join(words),'words':words}


def TextRelatedness(first_text,second_text,USE_ENCODER,session,embedded_text,text_input):
    first_text = text_pre_process(first_text,remove_stopword = True,toLower = True,remove_punctuations_numbers=True,min_word_len=3)
    second_text = text_pre_process(second_text,remove_stopword = True,toLower = True,remove_punctuations_numbers=True,min_word_len=3)

    first_text_sentence = first_text['sentence']
    second_text_sentence = second_text['sentence']

    #models = generate_models_use([first_text_sentence,second_text_sentence],USE_ENCODER)
    models  = session.run(embedded_text, feed_dict={text_input: [first_text_sentence,second_text_sentence]})

    return VectorSimilarity(models[0],models[1])

def TextSimilarity(similarity_type,first_text,second_text,USE_ENCODER,session,embedded_text,text_input):
    if similarity_type=='relatedness': # similarity_type=='semantic', 'syntactic' , 'relatedness'
        return TextRelatedness(first_text,second_text,USE_ENCODER,session,embedded_text,text_input)
    else:
        return 0

def read_topics():
    topics = []
    topics_preprocessed = []
    with open('topics','r') as f_r:
        lines = f_r.readlines()
        for line in lines:
            line = line.strip()
            if line!="":
                topics.append(line)
                line = text_pre_process(line, remove_stopword=True, toLower=True,
                                              remove_punctuations_numbers=True, min_word_len=3)

                topics_preprocessed.append(line['sentence'])
    return topics,topics_preprocessed

def TopicsSimilarity(similarity_type,topics_model,topics,sentence,USE_ENCODER,session,embedded_text,text_input):
    sentence = text_pre_process(sentence,remove_stopword = True,toLower = True,remove_punctuations_numbers=True,min_word_len=3)
    sentence = sentence['sentence']

    sentence_model = session.run(embedded_text, feed_dict={text_input: [sentence]})[0]

    topics_weight = []
    for topic,topic_model in zip(topics,topics_model):
        topics_weight.append((topic,VectorSimilarity(sentence_model,topic_model)))

    topics_weight_sorted = sorted(topics_weight, key=lambda x: x[1],reverse=True)
    topic_weight_dict =[{pair[0]:pair[1]} for pair in topics_weight_sorted[:5]]
    return topic_weight_dict


def CheckRequestSource(request_):
    try:
        if (request_.headers['X-RapidAPI-Proxy-Secret'])!= RapidApi_key:
            return False
        else:
            return True
    except:
        return False
