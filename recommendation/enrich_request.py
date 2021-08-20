import sys
import os
import pandas as pd

sys.path.append("..")
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
	data_path = os.path.join(os.path.abspath('..'), DATA_PATH)
	df = pd.read_csv(data_path, sep='\t')[CSV_COLUMNS_TO_KEEP]
	_convert_data_types(df)
	return df


def _convert_data_types(df):
	df[NUMBER_REVIEWS_COL].fillna(0, inplace=True)
	df[REVIEW_SCORE_COL] = df[REVIEW_SCORE_COL].astype(float)
	df[NUMBER_REVIEWS_COL] = df[NUMBER_REVIEWS_COL].astype(int)


def get_input_genre(input_drama):
    drama_data = _load_data()
    found_genre = drama_data[drama_data.data[NAME_COL] == input_drama][GENRE_COL]
    if len(found_genre) > 0:
        return drama_data[drama_data.data[NAME_COL] == input_drama][GENRE_COL].values[0]  # only returns first value
    else:
        return None