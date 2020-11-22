from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


def _get_synopsis(soup):
	synopsis = soup.find('span', id="Synopsis")
	if synopsis is None:
		return None

	all_paragraphs = []
	first_p = synopsis.find_next('p')
	all_paragraphs.append(first_p.text)
	for p in first_p.next_siblings:
		if p.name == 'p':
			all_paragraphs.append(p.text)
		if p.name == 'h2':
			break
	return "".join(all_paragraphs)


def _get_rating(soup):
	rating = soup.find("div", {"class": "voteboxrate"})
	if rating is None:
		return None
	return rating.text


def _get_number_of_votes(soup):
	votes = soup.find("span", {"class": "rating-total"})
	if votes is None:
		return None
	return votes.text.split(" votes")[0].split('(')[1]


def _find_main_cast_tag(soup):
	main_cast_tag = soup.find('dt', text='Main Cast')
	if main_cast_tag is not None:
		return main_cast_tag.parent

	main_cast_tag = soup.find('dt', text='Main cast')
	if main_cast_tag is not None:
		return main_cast_tag.parent

	main_cast_tag = soup.find('h2', id='Cast')
	if main_cast_tag is not None:
		return main_cast_tag.parent

	return None


def _get_main_cast_actors(soup):
	# TODO: (1) this only work for pages with bullet points under a main cast "dt" element;
	# TODO: (1) fails on older pages like 'https://wiki.d-addicts.com/Forget_You_Remember_Love'
	# TODO: (2) pages like 'https://wiki.d-addicts.com/Revolutionary_Love' have actor name in Korean, parse it out
	# TODO: fails on: https://wiki.d-addicts.com/Amanza
	main_cast_tag = _find_main_cast_tag(soup)

	if main_cast_tag is None:
		return None

	main_cast_raw = ''
	for elem in main_cast_tag.next_siblings:
		if elem.name == 'ul':
			main_cast_raw = elem.text
			break
	main_cast_list = [cast_elem.split(' as ')[0] for cast_elem in main_cast_raw.split("\n")]
	return "|".join(main_cast_list)


def extract_other_details_from_drama_page(url):
	"""Example URLs:
	url = 'https://wiki.d-addicts.com/Ambition'
	url = 'https://wiki.d-addicts.com/Forget_You_Remember_Love'
	url = 'https://wiki.d-addicts.com/Love_Alarm'
	url = 'https://wiki.d-addicts.com/Revolutionary_Love'
	url = 'https://wiki.d-addicts.com/Radio_Romance'
	"""
	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')
	synopsis = _get_synopsis(soup)
	user_rating = _get_rating(soup)
	number_of_votes = _get_number_of_votes(soup)
	main_cast = _get_main_cast_actors(soup)
	return synopsis, user_rating, number_of_votes, main_cast


# def _write_other_details_to_file(input_file, output_file):
# 	other_details = []
# 	f = open(input_file, "r")
# 	for drama_link in f:
# 		url = "https://wiki.d-addicts.com" + drama_link
# 		print(url)
# 		synopsis, user_rating, number_of_votes, main_cast = extract_other_details_from_drama_page(url)
# 		other_details.append((synopsis, user_rating, number_of_votes, main_cast))
# 	column_names = ["synopsis", "user_rating", "number_of_votes", "main_cast"]
# 	pd.DataFrame(other_details, columns=column_names).to_csv(output_file, sep='\t', index=False)
#
#
# if __name__ == "__main__":
# 	year = "2019"
# 	input_file = "/Users/diana/drama/data/dramawiki_" + year + "_dramas.csv"
# 	output_file = "/Users/diana/drama/data/dramawiki_" + year + "_dramas_other_details.csv"
# 	_write_other_details_to_file(input_file, output_file)


