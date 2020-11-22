from data.drama_wiki.data_cleaning.utils import *

DATA_PATH = '/Users/diana/drama/data/'  # TODO change this
RAW_FILES_ENDING = 'extracted_fields.csv'
MAIN_DETAILS_PROCESS_COLS = ['genre', 'episodes', 'network', 'user_rating','number_of_votes', 'main_cast'] #'synopsis',
MAIN_NAME_COL = 'main_name'
MAIN_DETAILS_OUTPUT_COLS = [MAIN_NAME_COL] + MAIN_DETAILS_PROCESS_COLS
OUTPUT_FILE_PATH = os.path.join(DATA_PATH, 'clean_data_files/clean_fields.csv')


def clean_genre(raw_genre):
	return process_short_text_field(raw_genre)


def clean_episodes(raw_episodes):
	return process_numeric_field(raw_episodes)


def clean_network(raw_network):
	return process_short_text_field(raw_network)


def clean_synopsis():
	# TODO
	return


def clean_user_rating(raw_user_rating):
	return process_numeric_field(raw_user_rating)


def clean_number_of_votes(raw_number_of_votes):
	return process_numeric_field(raw_number_of_votes)


def clean_cast_member(cast_member):
	return cast_member.split("(")[0]


def clean_main_cast(raw_main_cast):
	if is_null_or_empty(raw_main_cast):
		return None
	main_cast = raw_main_cast.strip()
	cast_members = main_cast.split("|")
	cast_members = [g.strip().lower() for g in cast_members]
	cast_members = [clean_cast_member(g) for g in cast_members]
	return format_list_fields(cast_members)


if __name__ == "__main__":
	df = load_raw_data(DATA_PATH, RAW_FILES_ENDING, MAIN_DETAILS_OUTPUT_COLS)

	df['genre_clean'] = df.apply(lambda x: clean_genre(x.genre), axis=1)
	df['episodes_clean'] = df.apply(lambda x: clean_episodes(x.episodes), axis=1)
	df['network_clean'] = df.apply(lambda x: clean_network(x.network), axis=1)
	df['user_rating_clean'] = df.apply(lambda x: clean_user_rating(x.user_rating), axis=1)
	df['number_of_votes_clean'] = df.apply(lambda x: clean_user_rating(x.number_of_votes), axis=1)
	df['main_cast_clean'] = df.apply(lambda x: clean_main_cast(x.main_cast), axis=1)

	drop_raw_cols_and_rename_clean(df, MAIN_DETAILS_PROCESS_COLS)

	remove_duplicates(df, MAIN_NAME_COL)
	print(df.shape)

	df[MAIN_DETAILS_OUTPUT_COLS].to_csv(OUTPUT_FILE_PATH, sep='\t', index=False)

