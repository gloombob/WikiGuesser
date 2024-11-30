import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import random
import csv
from apikey import WIKIMEDIA_API_KEY, WIKIMEDIA_USER_AGENT

headers = {
  'Authorization': f'Bearer {WIKIMEDIA_API_KEY}',
  'User-Agent': f'{WIKIMEDIA_USER_AGENT}'
}

country = "US"

# final functions for game

# gets articles and correct answer
def start_game(article=None, views=None):
   # get the requests_list from requests.csv
   requests_list = get_requests_list()

   # article and views from the first answer can be passed on if given as args to start_game
   return get_two_articles_views(requests_list, article, views)

def main():
  # calls check_requests, runs if up-to-date
  if check_requests():
     requests_list = get_requests_list()
     first_article, first_views, second_article, second_views = get_two_articles_views(requests_list)
     compare_results(first_views, second_views)

# writes csv-file of top 1000 searches articles for last 30 days
def get_requests():
  with open ("requests.csv", "w", encoding="utf-8", newline="")  as csv_file:
    fieldnames = ("article", "views")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # request data for the last 30 days
    # write the date and each days data to the csv file, then continue with next day
    for i in range(30):
        # start at -1 (yesterday), go to -30 (last month)
        year, month, day = str(date.today() - relativedelta(days=1+i)).split("-")
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/{country}/all-access/{year}/{month:02}/{day:02}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            article_dict_list = response.json()["items"][0]["articles"]
            writer.writeheader()
            writer.writerow({"article": f"{date.today() - relativedelta(days=1+i)}"})
            for article in article_dict_list:
                writer.writerow({"article": str(article["article"]), "views": article["views_ceil"]})

# checks if requests are up-to-date, if not: get_requests is run to update data
def check_requests() -> bool:
  with open ("requests.csv", "r", encoding="utf-8") as file:
      request_date = file.readlines()[1].strip("\n").replace(",", "")
      if request_date != str(date.today()-relativedelta(days=1)):
        get_requests()
        print("Got requests")
        check_requests()

      else:
        print("Requests up to date")
        return True

# returns data from requests.csv as a list of dicts with "article: value, views: value" pairs
def get_requests_list() -> list:
  with open("requests.csv", "r", encoding="utf-8") as request_file:
        request_reader = csv.DictReader(request_file)
        return list(request_reader)

# gets a random article from the requests_list, which it takes as an argument
def get_article(requests_list: list) -> str:
  # chooses random article from list
  random_article = random.choice(requests_list)["article"]
  return random_article

# get the views for a certain article
def get_views(requests_list: list, article: str) -> int:
  views = 0
  # loops through each dict in requests_list
  for dictionary in requests_list:
    if article == dictionary["article"]: # if the random article is equal to a dictionaries article - value add to views the value of views: value in that dictionary entry
      views += int(dictionary["views"])

  # returns the summed amount of views for specific article in the requests_list
  return views

# gets 2 random articles and their views, if 1 article and its views are passed as an arg, they become the first_article/_views variable which is passed on
def get_two_articles_views(requests_list: list, article=None, views=0):
  # compare 2 new random articles
  if article == None:
    first_article = get_article(requests_list)
    first_views: int = get_views(requests_list, first_article)

    second_article = get_article(requests_list)
    second_views: int = get_views(requests_list, second_article)

    return first_article, first_views, second_article, second_views

  # compare 1 new article to the second article of the round before
  elif article != None:
    first_article = article
    first_views = views

    second_article = get_article(requests_list)
    second_views = get_views(requests_list, second_article)

    return first_article, first_views, second_article, second_views

# takes first_views and compares against second_views, takes guess and compares it to the correct answer
def compare_results(first_views: int, second_views: int, count: int=0, guess=0):
  if first_views >= second_views:
    correct = 1
  elif first_views < second_views:
    correct = 2

  if guess == 0:
    print("No guess")

  if guess == correct:
    updated_count = count + 1
    return "Correct!", updated_count

  else:
    return "Wrong!", count

if __name__ == "__main__":
  main()