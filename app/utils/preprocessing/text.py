""" Preprocessing text """
import codecs
# import os
import nltk
import numpy as np
# from nltk.corpus import brown
import pymystem3

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


def prepare_coords(coords: dict) -> dict:
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
  y_pos = np.arange(1, len(x_coord) + 1, 1)

  print(x_coord)
  print(y_coord)
  print(y_pos)
  return {'x': x_coord, 'y': y_coord, 'pos': y_pos}
