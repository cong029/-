from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import time

# 📅 오늘 날짜 출력
today = datetime.today().strftime("%Y-%m-%d")
print(f"📅 오늘 날짜: {today}")

# ✅ 팀 이름 입력 (소문자로 변환)
team_input = input("💬 확인할 팀 이름을 입력하세요 (엔터 누르면 전체 경기 출력): ").strip().lower()

# ✅ 크롬 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # ❗창 안 뜨게 하고 싶으면 이 줄 주석 해제
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--lang=ko_KR")
chrome_options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=chrome_options)

# ✅ 경기 일정 페이지 접속
url = f"https://m.sports.naver.com/kbaseball/schedule/index?date={today}"
driver.get(url)

# ✅ 페이지 로딩 대기 (예외 처리 포함)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ScheduleAllType_match_list__3n5L_"))
    )
except TimeoutException:
    print("⚠️ 페이지 로딩이 너무 느립니다. 데이터를 가져오지 못했어요.")
    driver.quit()
    exit()

# ✅ HTML 파싱
soup = BeautifulSoup(driver.page_source, "html.parser")
games = soup.select("ul.ScheduleAllType_match_list__3n5L_ > li")

match_count = 0
for game in games:
    time_tag = game.select_one(".MatchBox_time__nIEfd")
    status_tag = game.select_one(".MatchBox_status__2pbzi")
    teams = game.select(".MatchBoxHeadToHeadArea_team__40JQL")
    pitchers = game.select(".MatchBoxHeadToHeadArea_item__1IPbQ")

    if len(teams) == 2 and time_tag and status_tag:
        team1 = teams[0].get_text(strip=True)
        team2 = teams[1].get_text(strip=True)
        pitcher1 = pitchers[0].get_text(strip=True) if len(pitchers) > 0 else "-"
        pitcher2 = pitchers[1].get_text(strip=True) if len(pitchers) > 1 else "-"
        game_time = time_tag.get_text(strip=True)
        status = status_tag.get_text(strip=True)

        # ✅ 소문자로 비교
        if team_input == "" or team_input in [team1.lower(), team2.lower()]:
            print("⚾", game_time, f"{team1}({pitcher1}) vs {team2}({pitcher2}) - {status}")
            match_count += 1

if match_count == 0:
    print("📄 오늘 예정된 경기가 없습니다.")

driver.quit()
