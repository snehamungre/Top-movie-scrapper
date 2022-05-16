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
    moviePage = get_top_year_page(year)
    movieList = moviePage.findAll('div', attrs={'class': 'lister-item mode-advanced'}, limit=5)
    i = 1
    for divItem in movieList:
        div = divItem.find('div', attrs={'class': 'lister-item-content'})
        header = div.findChildren('h3', attrs={'class': 'lister-item-header'})
        title = (header[0].findChildren('a'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore')
        genre = ((div.findChildren('p'))[0].findChildren('span', attrs={'class': 'genre'}))[0].string
        ratingBar = div.findChildren('div', attrs={'class': 'ratings-bar'})
        rating = ratingBar[0].findChildren('div', attrs={'class': 'inline-block ratings-imdb-rating'})
        print(str(i) + ". " +
              str(title) + " - " +
              str((rating[0].findChildren('strong'))[0].contents[0].encode('utf-8').decode('ascii', 'ignore'))
              + "    " + str(genre))

        i += 1


def get_top_movies_range(start_year, end_year):
    """
    It gets the movies for the required years as inputted by the user
    :param start_year:
    :param end_year:
    :return: csv file with the list of the top 5 movies of the year range provided
    """
    for i in range(start_year, end_year + 1):
        print(str(i) + " (Movie - Rating)")
        get_top_movies(i)
        print(" ")


if __name__ == '__main__':
    print("Give a range of years?")
    start = 0
    end = 0
    condition = 1
    while condition:
        print("start")
        start = int(input())
        print("end")
        end = int(input())
        print("--- results ---")
        if start < end:
            condition = 0
        else:
            print("Give a range of years? Start and then the end")
    get_top_movies_range(start, end)
