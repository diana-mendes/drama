from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


def _get_synopsis(soup):
	all_paragraphs = []
	first_p = soup.find('span', id="Synopsis").find_next('p')
	all_paragraphs.append(first_p.text)
	for p in first_p.next_siblings:
		if p.name == 'p':
			all_paragraphs.append(p.text)
		if p.name == 'h2':
			break
	return "".join(all_paragraphs)


def _get_rating(soup):
	return soup.find("div", {"class": "voteboxrate"}).text


def _get_number_of_votes(soup):
	votes_text = soup.find("span", {"class": "rating-total"}).text
	return votes_text.split(" votes")[0].split('(')[1]


def _get_main_cast_actors(soup):
	# TODO: this only work for pages with bullet points under a main cast "dt" element;
	# TODO: fails on older pages like 'https://wiki.d-addicts.com/Forget_You_Remember_Love'
	main_cast = soup.find('dt', text='Main Cast').parent
	main_cast_raw = ''
	for elem in main_cast.next_siblings:
		if elem.name == 'ul':
			main_cast_raw = elem.text
			break
	main_cast_list = [cast_elem.split(' as ')[0] for cast_elem in main_cast_raw.split("\n")]
	return "|".join(main_cast_list)


if __name__ == "__main__":
	# url = 'https://wiki.d-addicts.com/Ambition'
	# url = 'https://wiki.d-addicts.com/Forget_You_Remember_Love'
	# url = 'https://wiki.d-addicts.com/Love_Alarm'
	url = 'https://wiki.d-addicts.com/Radio_Romance'
	html = urlopen(url)
	soup = BeautifulSoup(html, 'html.parser')
	synopsis = _get_synopsis(soup)
	user_rating = _get_rating(soup)
	number_of_votes = _get_number_of_votes(soup)
	main_cast = _get_main_cast_actors(soup)
	print(synopsis)
	print(user_rating, number_of_votes)
	print(main_cast)




