""" Preprocessing text """
import codecs
# import os
import nltk
import numpy as np
# from nltk.corpus import brown
import pymystem3
from collections import OrderedDict

nltk.download('punkt')
nltk.download('stopwords')


def save_bag_of_words(path: str):
  """ algorithm preprocessing text """
  stop_words = nltk.corpus.stopwords.words('russian')
  mystem = pymystem3.Mystem()

  file_object = open('temp/preprocessing/bag_of_words.txt',
                     'w',
                     encoding="utf-8")

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
