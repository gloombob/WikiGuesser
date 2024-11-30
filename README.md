# WikiGuesser
#### Video Demo: https://youtu.be/wdUsIeRiqpA
#### Description:
This is a fun and simple guessing game that lets you explore the latest Wikipedia trends.
Your task is to guess which of two randomly selected Wikipedia articles has been viewed more often in the past 30 days. The program includes the option to open up Wikipedia articles in your browser that appear interesting as well as a scoreboard to track your best runs.

#### How to Play
Hint: You need to run **gui.py** to run the program. In order to use the program, you need to register your own personal API token for wikimedia (https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs). Both an authorization key and an user agent can be provided by wikimedia and have to be provided to **headers** in project.py so that requests can be made.  

To run the game, you'll have to install some Python libraries. Check the **requirements.txt** file for all necessary libraries. 
1. After starting the game, two article names will appear on buttons.
2. Click the button for the article you think was viewed more often.
3. For each correct guess, your score increases by 1.
4. An incorrect guess ends the game, but you’ll have the option to save your score by entering your name.



### File structure
The program is structured in the following files:
* project.py: core functionality
* gui.py: implements GUI using the CustomTkinter library
* test_project.py: contains unit tests for project.py, using pytest
* requests.csv: stores top 1000 most-viewed articles and their view counts for last 30 days
* scoreboard.csv: tracks the top 10 high scores

### project.py
Includes main functionality of the program.
Functions for requesting Wikipedia view data via the **wikimedia API**. 

##### get_requests()

The most important function is the **get_requests function**. This functions requests data from the wikimedia API using a header with an Authorization key and an User-Agent. The data used is the top 1000 Wikipedia articles viewed each day.

Data is requested for the last 30 days. The function writes the date of the day in YYYY-MM-DD format and then the corresponding data, one row each for every article and its views on that day.

##### get_article(), get_views() and get_two_articles_views()

**get_article()** chooses a random article name from the requests.csv data and returns the article name.

**get_views()** takes an article as input and sums up the views for the article over the last 30 days. Returns total view count for the given article.

**get_two_articles_views()** fetches two articles and their view counts. If an article and its view count are provided, the function will use this as the first article and only get one randomly chosen second article.

### gui.py
Provides a simple GUI for the program using the **CustomTkinter** library, which builds upon the standard Tkinter library.
The GUI defines different frames that represent different "windows" within the program.

The GUI is structured using python **classes**, following best practices for scalability.

**MainWindow class**

This is the "root" or "parent" class to all other classes used in the GUI. It sets up the window and mainloop for the GUI. All frames used in the GUI are initialized here to be easily accessible.

The MainWindow class has the switch_to_frame() function, which allows to easily switch between the frames when required.

**GameFrame class**

This is the window where the game takes place. Two buttons with the article names let you choose your guess.

Bellow each button are additional buttons to open the article on Wikipedia.
**ScoreboardFrame class**

This is the window where the scoreboard is displayed using a CTkTable.

**GameoverFrame class**

This is the window that is raised after guessing incorrectly. Here you can enter a name and save your score, play again or return to the start menu.


### test_project.py
Includes tests for the most important functions of project.py using **pytest**.

### requests.csv
This file contains data for the top 1000 most-viewed Wikipedia articles in the United States over the last 30 days. The data is structured as follows:

Each row includes the article name and the number of views in the format:
article, views

The date is recorded in the YYYY-MM-DD format and appears as a standalone row preceding the data for each day.
### scoreboard.csv
Contains the names and score of the top 10 runs. Each row includes name and score (number of correct guesses) in the format:
name, score

