import requests
from bs4 import BeautifulSoup


def get_top_year_page(year):
    """
    It gets the movies for the required year
    :param year: year for which we are getting the top 5 movies for
    :return: csv file with the list of the top 5 movies of the year range provided
    """
    url = "https://www.imdb.com/search/title/?title_type=feature&release_date=" + str(year) + "-01-01," \
          + str(year) + "-12-31"

    response = requests.get(url)
    # check if the request was successful
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))

    movie_doc = BeautifulSoup(response.text, 'html.parser')
    return movie_doc


def get_top_movies(year):
    moviePage = get_top_year_page(year);
    movieList = moviePage.findAll('div', attrs={'class': 'lister-item mode-advanced'}, limit=5)
    i = 1
    for divItem in movieList:
        div = divItem.find('div', attrs={'class':'lister-item-content'})
        header = div.findChildren('h3', attrs={'class': 'lister-item-header'})
        print(str(i) + ". " + str((header[0].findChildren('a'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore')))
        i += 1


def get_top_movies_range(start_year, end_year):
    """
    It gets the movies for the required years as inputted by the user
    :param start_year:
    :param end_year:
    :return: csv file with the list of the top 5 movies of the year range provided
    """
    for i in range(start_year, end_year + 1):
        print(i)
        get_top_movies(i)


if __name__ == '__main__':
    print("Give a range of years?")
    print("start")
    start = int(input())
    print("end")
    end = int(input())
    get_top_movies_range(start, end)

