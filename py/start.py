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
        print(read_book_id)

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

def start():
    title = ""
    book_id = 0
    avg_rating = 0
    user_dict = {}
    genre_list = []
    count = 0
    weighted_total = 0
    
    # Display a prompt and get user input
    search_string = input("Enter your book title: ")

    book_dict = get_book_id(search_string)
    book_id = next(iter(book_dict))
    title = book_dict[book_id]
    print('Title:', title)
    avg_rating = get_book_rating_avg(book_id)
    print('Avg Rating:', avg_rating)
    user_dict = get_user_dict(book_id)
    genre_list = get_book_genres(book_id)

    for user_id, og_rating in user_dict.items():
        user_genre_rating = get_user_genre_rating(user_id,genre_list)
        if og_rating > user_genre_rating:
            weighted_rating = og_rating + ((og_rating - user_genre_rating) / (user_genre_rating / 5))
        elif og_rating < user_genre_rating:
            weighted_rating = user_genre_rating * (og_rating / 5)
        else:
            weighted_rating = og_rating

        weighted_total += weighted_rating 
        count += 1

    if count > 0:
        avg_weighted_rating = round(weighted_total/count, 2)
    print('Avg Weighted Rating:', avg_weighted_rating)

start()