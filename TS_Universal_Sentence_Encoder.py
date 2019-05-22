import tensorflow as tf
import tensorflow_hub as hub
import time

def read_USE_model():
  module_url = 'https://tfhub.dev/google/universal-sentence-encoder-large/3'
  return hub.Module(module_url)


def init_USE():
  # Create graph and finalize (finalizing optional but recommended).
  g = tf.Graph()
  with g.as_default():
    # We will be feeding 1D tensors of text into the graph.
    text_input = tf.placeholder(dtype=tf.string, shape=[None])
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
    embedded_text = embed(text_input)
    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
  g.finalize()

  # Create session and initialize.
  session = tf.Session(graph=g)
  session.run(init_op)
  return session,embedded_text,text_input

def generate_models_use(list_of_sentences,encoder):
  '''
  This function generates the feature vectors of the input sentences.
  :param list_of_sentences:
  :param embed:
  :return:
  '''
  messages  = list_of_sentences

  with tf.Session() as session:
    session.run([tf.global_variables_initializer(), tf.tables_initializer()])
    message_embeddings = session.run(encoder(messages))

  models = []
  for message_embedding in message_embeddings:
    models.append([float(x) for x in message_embedding])
  return models

# start_time = time.time()
# encoder = read_USE_model()
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
# start_time = time.time()
# session,embedded_text,text_input =  init_USE()
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
#
#
# start_time = time.time()
#
# generate_models_use(['hello'],encoder)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
#
# result = session.run(embedded_text, feed_dict={text_input: ['hello']})
# print(result)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
# start_time = time.time()
#
# generate_models_use(['hello'],encoder)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
#
# generate_models_use(['hello'],encoder)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
# start_time = time.time()
#
# generate_models_use(['hello'],encoder)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
#
# start_time = time.time()
#
# generate_models_use(['hello'],encoder)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
