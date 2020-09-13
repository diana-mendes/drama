from bs4 import BeautifulSoup
from urllib.request import urlopen


def _get_drama_urls_from_year_list(drama_list_url):
    """
    Gets links from this list and manually save them to CSV (exclude urls at the start and end of the list).
    Example usage:
        url = "https://wiki.d-addicts.com/Category:KDrama2019"
        _get_drama_urls_from_year_list(url)
    """
    html = urlopen(drama_list_url)
    soup = BeautifulSoup(html, 'html.parser')
    list_items = soup.find_all('li')
    for li in list_items:
        if len(li.contents) == 1:
            link = li.find('a')
            if link is not None:
                print(link['href'])


if __name__ == "__main__":
    year_drama_list_url = 'https://wiki.d-addicts.com/Category:KDrama2019'
    _get_drama_urls_from_year_list(year_drama_list_url)
    print("\n\n\n From the list above copy the drama urls to ~/Desktop/drama_reco/dramawiki_[year]_dramas.csv")
