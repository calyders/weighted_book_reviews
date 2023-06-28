from bs4 import BeautifulSoup
import requests
import json
import feedparser

def get_book_id(search):
    book_id = 0
    book_dict = {}

    # URL of the website
    url = f"https://www.goodreads.com/search?q={search}"

    # Send a GET request to the website
    response = requests.get(url)

    # Get the HTML content
    html = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Using find_all()
    results = soup.find_all('div', class_="u-anchorTarget")
    a_results = soup.find_all('img', class_="bookCover")

    # Iterate over the elements found
    for result in results:
        book_id = result.get('id')
        for a_result in a_results:
            title = a_result.get('alt')
            break

        #Adding to dict
        book_dict[book_id] = title
        break
    return(book_dict)

def get_book_rating_avg(book_id):
    rating_value = 0

    # URL of the website
    url = f"https://www.goodreads.com/book/show/{book_id}"

    # Send a GET request to the website
    response = requests.get(url)

    # Get the HTML content
    html = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Using find_all()
    meta_datas = soup.find_all('script', type="application/ld+json")

    # Iterate over the elements found
    for meta_data in meta_datas:
        # Parse the JSON string
        parse = json.loads(meta_data.text)
        # Access the parsed data
        agg_rating = parse["aggregateRating"]
        agg_rating = json.dumps(agg_rating)
        # Parse the JSON string
        parse2 = json.loads(agg_rating)
        # Access the parsed data
        rating_value = parse2["ratingValue"]
        break

    return(rating_value)

def get_book_genres(book_id):
    genre_list = []

    # URL of the website
    url = f"https://www.goodreads.com/book/show/{book_id}"

    for i in range(4):
        # Send a GET request to the website
        try:
            response = requests.get(url)
            if not response:
                print('NO response')
                continue
            # Additional processing of the response
        except:
            print("Request error occurred")
            continue        

        # Get the HTML content
        html = response.text
        if not html:
            print('NO HTML')
            continue

        # Create a BeautifulSoup object
        try:
            soup = BeautifulSoup(html, 'html.parser')
            if not soup:
                print('NO SOUP')
                continue
        except:
            print('SOUP failed')
            continue

        # Using find_all()
        try:
            genre_headers = soup.find_all('span', class_='BookPageMetadataSection__genreButton')
            if not genre_headers:
                print('NO genre_headers')
                continue
            else:
                break
        except:
            print('Genre headers failed')
            continue

    # Iterate over the elements found
    for genre_header in genre_headers:
        genre = genre_header.find('span', class_='Button__labelItem').text
        if not genre:
            print('NO GENRE FOUND')
        genre_list.append(genre)
        
    return(genre_list)