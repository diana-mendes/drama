import sys
import pandas as pd
import tensorflow as tf

from .enrich_request import get_input_genre

# TODO: change these to local paths
VOCAB_PATH = 'resources/genre_one_hot_encoder_vocab.csv'
GENRE_ONE_HOT_LOOKUP_PATH = 'resources/genre_one_hot_lookup.csv'
NAME_COL = 'main_name'

def load_one_hot_vectors(lookup_path):
  return pd.read_csv(lookup_path, index_col=NAME_COL)


def lookup_genres_from_one_hot_vector(genre_one_hot, vocab):
  """
  Returns genre list from genre one hot encoded vector.
  """
  return [x for (x, y) in zip(vocab, genre_one_hot) if y == 1]


def _get_top_k(cosine_simil, k):
  return cosine_simil.argsort()[-k:]


def _print_info(request, selected_drama_names, vocab, one_hot_selected_dramas):
  print("Genre of request:", 
        lookup_genres_from_one_hot_vector(request[0], vocab))
  
  for i in range(len(selected_drama_names)):
    print("Drama", i)
    print("Name:", selected_drama_names[i])
    
    selected_drama_genre_one_hot = one_hot_selected_dramas[i, :]
    print("One hot encoding of genre: ", selected_drama_genre_one_hot)
    print("Genre:", 
          lookup_genres_from_one_hot_vector(selected_drama_genre_one_hot, vocab))


def calculate_cosine_similarity_and_retrieve_top_k(request, all_data, k, debug=False, vocab=None):
  from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
  
  drama_names = all_data.index
  features = all_data.values

  cosine_simil = sklearn_cosine_similarity(request, features)[0]
  top_k_indices = _get_top_k(cosine_simil, k)
  
  if debug:
    if vocab is None:
      raise ValueError("Must pass vocab in debug mode.")

    selected_drama_names = drama_names[top_k_indices]
    one_hot_selected_dramas = features[top_k_indices, :]
    _print_info(request, selected_drama_names, vocab, one_hot_selected_dramas)
  
  # return names
  return drama_names[top_k_indices].tolist()
  

def get_genre_one_hot_encoder_model():  # TODO: implement training encoder somewhere else
  """
  Returns Genre one hot encoder model, loads pre-fitted genre vectorizer layer.
  """
  textVectorizer = tf.keras.layers.experimental.preprocessing.TextVectorization(output_mode='binary')
  
  vocab = read_genre_vocab(VOCAB_PATH)
  load_genre_vectorizer_layer(textVectorizer, vocab)
  
  model = tf.keras.models.Sequential()
  model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
  model.add(textVectorizer)

  return model


def load_genre_vectorizer_layer(layer, vocab):
  """
  Sets `vocab` as the vocabulary of `layer`.
  
  :param layer: tf.keras.layers.experimental.preprocessing.TextVectorization
  :param vocab: List of strings (vocabulary elements)
  
  :return tf.keras.layers.experimental.preprocessing.TextVectorization 
  """
  layer.set_vocabulary(vocab)


def read_genre_vocab(vocab_path):
  """
  Reads vocabulary for genre one hot encoder from CSV file. 
  CSV file must have no header.
  Each element of vocabulary must be in its separate lines.
  """
  try:
    vocab = pd.read_csv(vocab_path, header=None)[0].values.tolist()
  except ValueError:
      print("""VOCAB_PATH not found, please retrain the genre model with 
      get_genre_one_hot_encoder_model(train=True, overwrite_vocab=True)""")
  return vocab[1:]  # index 0 is OOV token


def load_one_hot_vectors(lookup_path):
  return pd.read_csv(lookup_path, index_col=NAME_COL)


class GenreRecommendation:
    def __init__(self):
        self.genre_one_hot_model = get_genre_one_hot_encoder_model()

    def get_genre_recommendation(self, input_drama, k=3):
        genre = get_input_genre(input_drama)
        if genre is None:
          return []
        genre_one_hot = self.genre_one_hot_model.predict(genre)

        # get top dramas
        all_data_genre_one_hot = load_one_hot_vectors(GENRE_ONE_HOT_LOOKUP_PATH)
        vocab = read_genre_vocab(VOCAB_PATH)

        return calculate_cosine_similarity_and_retrieve_top_k(genre_one_hot, 
                                                            all_data_genre_one_hot, 
                                                            k,
                                                            debug=True,
                                                            vocab=vocab)
