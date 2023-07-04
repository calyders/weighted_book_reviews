# Weighted Book Review Web App
### Project Description
The idea for this project was to use Python to create a web application capable of retrieving online book reviews and calculating a weighted average review score for each book based on individual user ratings within the corresponding genre. This application will provide a valuable tool for book enthusiasts and help them make informed decisions about their reading choices.

### How It Works
The web application utilizes Python's powerful web scraping capabilities to fetch book reviews from various online platforms and sources, such as popular book review websites, social media platforms, and forums. By leveraging libraries like BeautifulSoup and Requests, the application can efficiently extract relevant information, including the book's title, author, genre, and user ratings.

![image](https://github.com/calyders/weighted_book_reviews/assets/115501756/05f6f7e9-0700-441c-a20f-53b771e0fd8b)

To determine the weighted average review score, the application will search user profiles found in the reviews section, collecting their average ratings for other books within the same genre as the one searched in the web app. The application will then analyze the ratings of these users in the same genre and calculate a weighted average, giving more weight to users who have demonstrated a higher level of expertise or reliability based on their past ratings.

### Results
By implementing this project, users will have access to a comprehensive platform where they can find aggregated reviews and reliable average scores for books in different genres. This will empower them to make more informed decisions when selecting their next read, as they can rely on the collective opinions of users who share similar tastes and preferences.

### Final Thoughts
The project accomplishes the simple goal set in the beginning to provide a weighted review for specific books, allowing for more insightful book purchasing by users. With a solid foundation set in the code here, more functionalities can be added down the line, such as the ability to return average weighted scores per genre for individual reviewers, not just the book. This would enable the user to determine for themself whether a certain review should be considered reliable or not. Perhaps in the future, an HTML graphical user interface will be added for non-technically inclined interested parties.
