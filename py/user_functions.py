from bs4 import BeautifulSoup
import requests
import json
import feedparser
from book_functions import get_book_genres

def get_user_dict(book_id):
    a_tag = ""
    href_tag = ""
    href_columns = ""
    user_id = ""
    user_dict = {}

    # URL of the website
    url = f"https://www.goodreads.com/book/show/{book_id}"

     # Send a GET request to the website
    response = requests.get(url)

    # Get the HTML content
    html = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Using find_all()
    results = soup.find_all('article', class_="ReviewCard")

    # Iterate over the elements found
    for result in results:
        profile_name = result.find('div', class_="ReviewerProfile__name")
        a_tag = profile_name.find('a')
        href_tag = a_tag.get('href')
        href_columns = href_tag.split('/')
        user_id = href_columns[-1]

        #Get User Rating
        rating_star = result.find('span', class_="RatingStars")
        span_tag = rating_star.get('aria-label')
        span_columns = span_tag.split(' ')
        user_rating = span_columns[1]

        #Adding to dict
        user_dict[user_id] = float(user_rating)
        
    return(user_dict)

def get_user_genre_rating(user_id,genre_list):
    rating_total = 0
    count = 0
    avg_rating = 0
    user_rating = 0
    read_book_id = ""

    user_url = f"https://www.goodreads.com/review/list_rss/{user_id}?shelf=read"
    feed = feedparser.parse(user_url)

    # Iterate over the entries/items in the feed
    for entry in feed.entries:
        #Get read book id
        read_book_id = entry.get('book')['id']
        if not read_book_id:
            print('NO Book ID')
            continue

        #get genre list of read book
        read_book_genre_list = get_book_genres(read_book_id)
        if not read_book_genre_list:
            print('NO Read Book Genre List')
            continue
        matches = len(set(genre_list).intersection(read_book_genre_list))
        if matches >= 1:
            user_rating = float(entry.get('user_rating'))
            if user_rating:
                rating_total += user_rating + (matches/10)
                count += 1

    if count > 0:
        avg_rating = round(rating_total/count, 2)
    
    return(avg_rating)