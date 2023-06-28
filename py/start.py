from bs4 import BeautifulSoup
import requests
import json
import feedparser
import user_functions as uf
import book_functions as bf

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

    book_dict = bf.get_book_id(search_string)
    book_id = next(iter(book_dict))
    title = book_dict[book_id]
    print('Title:', title)
    avg_rating = bf.get_book_rating_avg(book_id)
    print('Avg Rating:', avg_rating)
    user_dict = uf.get_user_dict(book_id)
    genre_list = bf.get_book_genres(book_id)

    for user_id, og_rating in user_dict.items():
        user_genre_rating = uf.get_user_genre_rating(user_id,genre_list)
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