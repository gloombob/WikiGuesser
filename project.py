import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import random
import csv

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJjZjY5Zjg4ZjU0ZTFiNmQ2MTg2MmMxZjkyMmFhN2I4MSIsImp0aSI6IjFhOTNiYWIzMTU5NmEyNmI0ZGU4ZTRkYTg3OWI4MzhkMTFiZjg5M2UxZjkyM2FlZDNkODBkNzQ3Y2MzOTlkMzM5M2VjNDVjNDZkMWZmM2MyIiwiaWF0IjoxNzE5ODY0MTQ1Ljc4MTc4MywibmJmIjoxNzE5ODY0MTQ1Ljc4MTc4NywiZXhwIjozMzI3Njc3Mjk0NS43Nzg1OCwic3ViIjoiNzU5ODk2ODQiLCJpc3MiOiJodHRwczovL21ldGEud2lraW1lZGlhLm9yZyIsInJhdGVsaW1pdCI6eyJyZXF1ZXN0c19wZXJfdW5pdCI6NTAwMCwidW5pdCI6IkhPVVIifSwic2NvcGVzIjpbImJhc2ljIl19.P_do81AQInSEp90iil0btMzywWZxzloLBGtu-pQn3e-qnUh1PstK90jpvzPDo3D_d1E12Xe1Dp3_rEOianL6AJTmrkntLTVKD-QPHLMbiSR2EymEUL_cMFyTlLbTXrXdUc7jJig8uc7mmpCr24qDa-_6sLI9suy-r5EJTcCIy5jkgZJVaORfGgQ_NG2wRuF6-5xJyX6AgUCUTRz9YePJsP74vltVjcT-e8s3iFMof_BtCWe64xzDqPjIfas6XQNTKyyM1EnjPoKrIKiAvQ6OpxBCZvly5V4z3_As5uPuq7-8zltmmAb03boeI9PUay35twkVkgMiRgzgeIteVUzwUmjmBBeRFwfEDr4JUI8gte3dih4v-8kCJvkAg3f-5F2pl56hsxs44ty8gUuoUGMV3soRyYAsWWvnFYvKaucyPbQfGXhpcX1lID7uV2ZXFtIUARJHasU8yAzk742ViB-g74H1hYfoBSaiowaH0ddpmXnx5Nzfb5reDj-M6Kh0yKT2idDxOedOaP9LdomK8U31sF6x1L845S4REQoxKG4TE9NK51B3QHXJV2nfIPfJxfqCO1GjgxfVKAL8qk9oKopP3dyIecbd1D60DyMm1ckgw7f3N8p_0AEcMnmWG2ipZ7VaC0F2ysFp0lnmgIxzu5jhFEGFs_xOyeFVtGeOd9Te4vQ',
  'User-Agent': 'WikiGuesser'
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