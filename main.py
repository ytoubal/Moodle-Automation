import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get("https://moodle.polymtl.ca/login/index.php")
time.sleep(3)

username = browser.find_element(By.ID, "username")
password = browser.find_element(By.ID, "password")

username.send_keys("ENTER USERNAME")
password.send_keys("ENTER PASSWORD")

login_attempt = browser.find_element(By.XPATH, "//*[@type='submit']")
login_attempt.submit()
time.sleep(3)

courses = browser.find_elements(By.CLASS_NAME, "coursename")
coursinf8775 = None
for i,course in enumerate(courses):
    if "INF8775" in course.text:
        coursinf8775 = course
coursinf8775.click()
time.sleep(3)

links = browser.find_elements(By.CLASS_NAME, "aalink" )
videos_number = []
for i,link in enumerate(links):
    if "capsule" in link.text:
        videos_number.append(link)

for i in range(len(videos_number)):
    
    links = browser.find_elements(By.CLASS_NAME, "aalink" )
    videos = []
    for link in links:
        if "capsule" in link.text:
            videos.append(link)

    videos[i].click()
    video_link = browser.find_element(By.TAG_NAME, "source").get_property("src")
    video_name = browser.find_element(By.CSS_SELECTOR, "#region-main h2").text

    cookies = browser.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    response = s.get(video_link, stream=True)
    with open(video_name+".mp4",'wb') as f:
        f.write(response.content)
    browser.back()
    time.sleep(2)