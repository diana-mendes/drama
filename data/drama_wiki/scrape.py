import pandas as pd
from data.drama_wiki.main_details import extract_main_details_from_drama_page
from data.drama_wiki.other_details import extract_other_details_from_drama_page


def scrape_dramas_from_year_list(year):
	input_file = "/Users/diana/drama/data/dramawiki_" + year + "_dramas.csv"
	output_file = "/Users/diana/drama/data/dramawiki_" + year + "_dramas_extracted_fields.csv"

	f = open(input_file, "r")

	details = []
	for drama_link in f:
		url = "https://wiki.d-addicts.com" + drama_link
		print(url)

		main_name, title, genre, episodes, network, broadcast_period, airtime = \
			extract_main_details_from_drama_page(url)

		synopsis, user_rating, number_of_votes, main_cast = \
			extract_other_details_from_drama_page(url)

		details.append((main_name, title, genre, episodes, network, broadcast_period, airtime, synopsis, user_rating,
		                number_of_votes, main_cast))

	column_names = ["main_name", "title", "genre", "episodes", "network", "broadcast_period", "airtime",
	                "synopsis", "user_rating", "number_of_votes", "main_cast"]
	pd.DataFrame(details, columns=column_names).to_csv(output_file, sep='\t', index=False)


if __name__ == "__main__":
	details = []
	years = ["2019", "2020"]
	for year in years:
		scrape_dramas_from_year_list(year)


