import os
import pandas as pd

DATA_PATH = 'data/'

NAME_COL = 'main_name'
GENRE_COL = 'genre'
CSV_COLUMNS_TO_KEEP = [NAME_COL, GENRE_COL]

# TODO: merge other details to add score and filter by it


def _load_data():
	"""
	Loads data for recommendation from CSV files.
	:return: pd.DataFrame with CSV_COLUMNS_TO_KEEP for all data found
	"""
	files = [f for f in os.listdir(DATA_PATH) if 'main_details.csv' in f]

	all_data = []
	for f in files:
		df = pd.read_csv(os.path.join(DATA_PATH, f), sep='\t')
		all_data.append(df[CSV_COLUMNS_TO_KEEP])

	# do some info
	all_data_df = pd.concat(all_data, axis=0, ignore_index=True)
	all_data_df.columns = CSV_COLUMNS_TO_KEEP

	return all_data_df


class TopScoreRecommendation:
	def __init__(self):
		self.data = _load_data()

	def _get_input_genre(self, input_drama):
		return self.data[self.data[NAME_COL] == input_drama][GENRE_COL].values[0]  # only returns first value

	def get_top_recos(self, input_drama, k=3):
		genre = self._get_input_genre(input_drama)
		genre_candidates = self.data[(self.data[GENRE_COL] == genre) & (self.data[NAME_COL] != input_drama)]

		return genre_candidates[NAME_COL].head(k).tolist()
