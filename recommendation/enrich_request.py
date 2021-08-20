import pandas as pd

DATA_PATH = 'data/clean_data_files/clean_fields.csv'

NAME_COL = 'main_name'
GENRE_COL = 'genre'
REVIEW_SCORE_COL = 'user_rating'
NUMBER_REVIEWS_COL = 'number_of_votes'
CSV_COLUMNS_TO_KEEP = [NAME_COL, GENRE_COL, REVIEW_SCORE_COL, NUMBER_REVIEWS_COL]


def _load_data():
	"""
	Loads data for recommendation from CSV files.
	:return: pd.DataFrame with CSV_COLUMNS_TO_KEEP for all data found
	"""
	df = pd.read_csv(DATA_PATH, sep='\t')[CSV_COLUMNS_TO_KEEP]
	_convert_data_types(df)
	return df


def _convert_data_types(df):
	df[NUMBER_REVIEWS_COL].fillna(0, inplace=True)
	df[REVIEW_SCORE_COL] = df[REVIEW_SCORE_COL].astype(float)
	df[NUMBER_REVIEWS_COL] = df[NUMBER_REVIEWS_COL].astype(int)


def preprocess_genre_data(df, keep_name_col=False):
  """
  """
  df = df[[NAME_COL, GENRE_COL]].dropna()
  formatted_genre_col = GENRE_COL+'_formatted'
  df[formatted_genre_col] = df[GENRE_COL].apply(lambda x: x.replace("|", " "))
  df.drop(GENRE_COL, axis=1, inplace=True)
  df.rename(columns={formatted_genre_col: GENRE_COL}, inplace=True)
  if keep_name_col:
    return df
  else:
    return df[GENRE_COL].values


def get_input_genre(input_drama):
    drama_data = _load_data()
    drama_data = preprocess_genre_data(drama_data, keep_name_col=True)

    found_genre = drama_data[drama_data[NAME_COL] == input_drama][GENRE_COL]
    if len(found_genre) > 0:
        return found_genre.values.tolist()
    else:
        return None