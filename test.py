from selenium import webdriver
import time

# 크롬 브라우저 자동 실행 (드라이버 경로 X)
driver = webdriver.Chrome()
driver.get("https://www.google.com")

time.sleep(3)
driver.quit()

