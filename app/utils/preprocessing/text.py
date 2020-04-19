""" Preprocessing text """
import codecs
# import os
import nltk
import numpy as np
# from nltk.corpus import brown
import pymystem3
from collections import OrderedDict
import artm
from ppretty import ppretty

nltk.download('punkt')
nltk.download('stopwords')

TARGET_FOLDER = 'temp/target_folder'
COLLECTION_PATH = 'temp/preprocessing/colletion.txt'
BAG_OF_WORDS_PATH = 'temp/preprocessing/bag_of_words.txt'


def save_bag_of_words(path: str):
  """ algorithm preprocessing text """
  stop_words = nltk.corpus.stopwords.words('russian')
  mystem = pymystem3.Mystem()

  file_object = open(BAG_OF_WORDS_PATH, 'w', encoding="utf-8")

  text = " "
  #converterUTF8(filename)
  with codecs.open(path, encoding='UTF-8') as f_manager:
    for line in f_manager:
      if len(line) != 0:
        text = text + " " + line

    word = nltk.word_tokenize(text)
    word_ws = [w.lower() for w in word if w.isalpha()]
    word_w = [w for w in word_ws if w not in stop_words]

    lem = mystem.lemmatize((" ").join(word_w))
    lema = [w for w in lem if w.isalpha() and len(w) > 1]
    freq = nltk.FreqDist(lema)

    results = []
    results = [(key + ":" + str(val)) for key, val in freq.items() if val > 1]

    file_object.write("|text" + " " + (" ").join(results) + '\n')

  file_object.close()

  return freq.items()


def prepare_coords(coords: dict, title_doc) -> OrderedDict:
  """ Prepare coords for display graph """
  temp_c = []
  temp_d = []

  for key, val in coords:
    if val > 1:
      temp_c.append(val)
      temp_d.append(key)

  x_coord = []
  y_coord = []

  for k in np.arange(0, len(temp_c), 1):
    ind = temp_c.index(max(temp_c))
    x_coord.append(temp_c[ind])
    y_coord.append(temp_d[ind])
    del temp_c[ind]
    del temp_d[ind]

  x_coord = x_coord[0:10]
  y_coord = y_coord[0:10]

  data_source = OrderedDict()
  chart_config = OrderedDict()

  chart_config["caption"] = "Частоты слов в документе " + title_doc.capitalize(
  )
  chart_config["yAxisName"] = "Количество слов"
  chart_config["theme"] = "gammel"

  data_source["chart"] = chart_config
  data_source["data"] = []

  for key, value in zip(y_coord, x_coord):
    data_source["data"].append({"label": key, "value": value})

  return data_source


def gluing_bag_of_words(docs):
  """ Gluing files """
  with open(COLLECTION_PATH, 'wt', encoding='utf8') as out:
    all_data = ''.join([
        open('{}'.format(item.text), encoding='utf8').read() for item in docs
    ])
    out.write(all_data)


def create_thematic_model(checked_list, num_topics, num_tokens, phi_tau,
                          theta_tau, decorr_tau):
  """ Create a thematic model """
  gluing_bag_of_words(checked_list)

  batch_vectorizer = artm.BatchVectorizer(data_path=COLLECTION_PATH,
                                          data_format='vowpal_wabbit',
                                          target_folder=TARGET_FOLDER,
                                          batch_size=len(checked_list))

  # batch_vectorizer = artm.BatchVectorizer(data_path=TARGET_FOLDER,
  #                                         data_format='batches')
  dictionary = artm.Dictionary(data_path=TARGET_FOLDER)
  model = artm.ARTM(
      num_topics=4,
      num_document_passes=len(checked_list),
      dictionary=dictionary,
      regularizers=[
          artm.SmoothSparsePhiRegularizer(name='sparse_phi_regularizer',
                                          tau=-1.0),
          artm.SmoothSparseThetaRegularizer(name='sparse_theta_regularizer',
                                            tau=-0.5),
          artm.DecorrelatorPhiRegularizer(name='decorrelator_phi_regularizer',
                                          tau=1e+5),
      ],
      scores=[
          artm.PerplexityScore(name='perplexity_score', dictionary=dictionary),
          artm.SparsityPhiScore(name='sparsity_phi_score'),
          artm.SparsityThetaScore(name='sparsity_theta_score'),
          artm.TopTokensScore(name='top_tokens_score', num_tokens=10)
      ])

  model.fit_offline(batch_vectorizer=batch_vectorizer,
                    num_collection_passes=len(checked_list))

  print(model.score_tracker['perplexity_score'].last_value)  # .last_value
  print(model.score_tracker['sparsity_phi_score'].last_value)  # .last_value
  print(model.score_tracker['sparsity_theta_score'].last_value)

  top_tokens = model.score_tracker['top_tokens_score']

  topic_dictionary = OrderedDict()

  for topic_name in model.topic_names:
    print(topic_name)
    list_name = []
    for (token, weight) in zip(top_tokens.last_tokens[topic_name],
                               top_tokens.last_weights[topic_name]):
      print(token, '-', round(weight, 3))
      list_name.append(token + '-' + str(round(weight, 3)))
    topic_dictionary[str(topic_name)] = list_name
