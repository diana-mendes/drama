from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

from data.drama_wiki.other_details import extract_other_details_from_drama_page

def _extract_list_contents_main_details(list_contents):
	contents_converted_to_string = []
	for elem in list_contents[1:]:
		if elem.string is not None and elem.string.string != '':
			contents_converted_to_string.append(elem.string)
	return ";".join(contents_converted_to_string)


def extract_main_details_from_drama_page(url):
	"""
	Extracts main details from drama page. Example input url: 'https://wiki.d-addicts.com/Hi_Bye_Mama!'
	"""
	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')
	(main_name, title, genre, episodes, network, broadcast_period, airtime) = \
		(None, None, None, None, None, None, None)
	main_name = soup.title.string.split(" - ")[0]
	for index, li in enumerate(soup.find_all('li')):
		bolded_item = li.find('b')
		if bolded_item is not None:
			list_item_name = li.contents[0].string
			list_contents = li.contents
			if len(list_contents) <= 1:
				continue
			if 'Title' in list_item_name:
				title = _extract_list_contents_main_details(list_contents)
			if 'Genre' in list_item_name:
				genre = _extract_list_contents_main_details(list_contents)
			if "Episodes" in list_item_name:
				episodes = _extract_list_contents_main_details(list_contents)
			if "Broadcast network" in list_item_name:
				network = _extract_list_contents_main_details(list_contents)
			if "Broadcast period" in list_item_name:
				broadcast_period = _extract_list_contents_main_details(list_contents)
			if "Air time" in list_item_name:
				airtime = _extract_list_contents_main_details(list_contents)
	return main_name, title, genre, episodes, network, broadcast_period, airtime


# def _write_main_details_to_file(input_file, output_file):
# 	main_details = []
# 	f = open(input_file, "r")
# 	for drama_link in f:
# 		url = "https://wiki.d-addicts.com" + drama_link
# 		print(url)
# 		main_name, title, genre, episodes, network, broadcast_period, airtime = \
# 			extract_main_details_from_drama_page(url)
# 		synopsis, user_rating, number_of_votes, main_cast = \
# 			extract_other_details_from_drama_page(url)
# 		main_details.append((main_name, title, genre, episodes, network, broadcast_period, airtime, synopsis,
# 		                     user_rating, number_of_votes, main_cast))
# 	column_names = ["main_name", "title", "genre", "episodes", "network", "broadcast_period", "airtime", "synopsis",
# 	                "user_rating", "number_of_votes", "main_cast"]
# 	pd.DataFrame(main_details, columns=column_names).to_csv(output_file, sep='\t', index=False)
#
#
#
# if __name__ == "__main__":
# 	year = "2020"
# 	input_file = "/Users/diana/Desktop/drama_reco/dramawiki_" + year + "_dramas.csv"
# 	output_file = "/Users/diana/Desktop/drama_reco/dramawiki_" + year + "_dramas_main_details.csv"
# 	_write_main_details_to_file(input_file, output_file)
