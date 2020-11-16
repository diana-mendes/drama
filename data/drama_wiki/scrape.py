from main_details import extract_main_details_from_drama_page
from other_details import extract_other_details_from_drama_page


if __name__ == "__main__":
	main_details = []
	year = "2020"
	input_file = "/Users/diana/Desktop/drama_reco/dramawiki_" + year + "_dramas.csv"
	output_file = "/Users/diana/Desktop/drama_reco/dramawiki_" + year + "_dramas_main_details.csv"

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
	                "synopsis"]
	pd.DataFrame(main_details, columns=column_names).to_csv(output_file, sep='\t', index=False)

