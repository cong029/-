from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
url = "https://m.sports.naver.com/kbaseball/schedule/index"
driver.get(url)
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

matches = soup.find_all("li", class_="MatchBox_match_item__3_D0Q")

for match in matches:
    teams = match.find_all("strong", class_="MatchBoxHeadToHeadArea_team__40JQL")
    time_tag = match.find("div", class_="MatchBox_time__nIEfd")

    if teams and time_tag:
        home = teams[0].text.strip()
        away = teams[1].text.strip()
        game_time = time_tag.text.strip()
        print(f"{home} vs {away} - {game_time}")

