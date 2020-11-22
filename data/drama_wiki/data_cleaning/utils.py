import pandas as pd
import re
import os


def is_null_or_empty(raw_input):
	if pd.isnull(raw_input) or raw_input.strip() == '':
		return True


def clean_two_word_elements(genre):
	split_chars = [' ', '/']
	for c in split_chars:
		genre_words = genre.split(c)
		if len(genre_words) > 1:
			return '-'.join([w.lower() for w in genre_words])
		else:
			return genre_words[0]


def process_short_text_field(input_text):
	if is_null_or_empty(input_text):
		return None
	raw_text = input_text.strip()
	text_elements = re.split(",| /| \|", raw_text)
	text_elements = [g.strip().lower() for g in text_elements]
	text_elements = [clean_two_word_elements(g) for g in text_elements]
	return format_list_fields(text_elements)


def process_numeric_field(input_text):  # todo: rename
	if not isinstance(input_text, str):
		input_text = str(input_text)
	if is_null_or_empty(input_text):
		return None
	clean_text = input_text.strip()
	if clean_text.isalpha():
		return None
	return clean_text


def format_list_fields(input_list):
	return "|".join(input_list)


def find_raw_data_files(data_path, common_filename_part):
	files = [f for f in os.listdir(data_path) if common_filename_part in f]
	return files


def load_raw_data(data_path, common_filename_part, cols):
	files = find_raw_data_files(data_path, common_filename_part)
	dfs = []
	for f in files:
		df = pd.read_csv(os.path.join(data_path, f), sep='\t')
		dfs.append(df[cols])
	all_data_df = pd.concat(dfs, axis=0, ignore_index=True)
	all_data_df.columns = cols
	return all_data_df


def remove_duplicates(df, cols):
	df[cols].drop_duplicates(inplace=True)


def drop_raw_cols_and_rename_clean(df, process_cols):
	for c in process_cols:
		df.drop(c, axis=1, inplace=True)
		clean_col_name = c + '_clean'
		df.rename(columns={clean_col_name: c}, inplace=True)
	return df
