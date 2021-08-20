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

WEIGHTED_SCORE_COL = 'weighted_score'


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


def _calculate_review_weighted_score(df):
	df['weight_factor'] = df.apply(lambda x: min(5, x[NUMBER_REVIEWS_COL])/5, axis=1)
	df[WEIGHTED_SCORE_COL] = df[REVIEW_SCORE_COL] * df['weight_factor']
	df.drop('weight_factor', axis=1, inplace=True)


class TopScoreRecommendation:
	def __init__(self):
		self.data = _load_data()

	def _get_input_genre(self, input_drama):
		found_genre = self.data[self.data[NAME_COL] == input_drama][GENRE_COL]
		if len(found_genre) > 0:
			return self.data[self.data[NAME_COL] == input_drama][GENRE_COL].values[0]  # only returns first value
		else:
			return None

	def get_top_recos_by_review_weighted_score(self, input_drama, k=3):
		genre = self._get_input_genre(input_drama)
		if genre is None:
			return []
		genre_candidates = self.data[(self.data[GENRE_COL] == genre) & (self.data[NAME_COL] != input_drama)].copy()
		if len(genre_candidates) == 0:
			return []
		_calculate_review_weighted_score(genre_candidates)
		recommended = genre_candidates.sort_values(by=WEIGHTED_SCORE_COL, ascending=False).head(k)
		print(recommended[CSV_COLUMNS_TO_KEEP])
		return recommended[NAME_COL].tolist()