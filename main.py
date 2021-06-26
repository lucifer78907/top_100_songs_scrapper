from bs4 import BeautifulSoup
import requests

# user_input = input("Which year you want to travel to ?"
#                    "\nType the date in YYYY-MM-DD Format\n")
# print(user_input)


# -------------------------------------SCRAPING USING Beautiful SOUP ---------------#
response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12")
web_data = response.text

soup = BeautifulSoup(web_data,"html.parser")

ele_list = soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")
names_list = [items.getText() for items in ele_list]
print(names_list)
