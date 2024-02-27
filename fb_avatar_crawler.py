import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Set ChromeDriver path
chrome_driver_path = "C:/Users/shihy/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe"
# Create Chrome WebDriver object
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the specified Facebook page
profile_url = "https://www.facebook.com/profile.php?id=100082098185374&sk=friends"
driver.get(profile_url)

input("Please manually log in to Facebook, then press the Enter key to continue...")

# Retrieve the username of the target profile
profile_name = driver.find_element(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w > div > div > span > h1").text.strip()
print(profile_name)

# Simulate scrolling to load more content
scroll = 0
while scroll < 500:  # The number of scrolls can be adjusted as needed
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)
    scroll += 1

friend_list = []
friend_elements = driver.find_elements(By.CSS_SELECTOR, "div.x1iyjqo2.x1pi30zi > div:nth-child(1) > a")
print('friend_elements:',len(friend_elements))
for element in friend_elements:
    friend_list.append({
        "to_url": element.get_attribute("href"),
        "to_name": element.text,
    })

json_string = json.dumps(friend_list)
file_path = 'output/friend_list.json'
with open(file_path, "w") as file:
    file.write(json_string)
print("The JSON string has been saved to a file:", file_path)

img_list = []
img_elements = driver.find_elements(By.CSS_SELECTOR, "div.x78zum5.x1q0g3np.x1a02dak.x1qughib > div > div > a")
print('img_elements:',len(img_elements))

for element in img_elements:
    img_list.append({
        "to_url": element.get_attribute("href"),
        "img_src":element.find_element(By.TAG_NAME, "img").get_attribute("src")
    })

json_string = json.dumps(img_list)
file_path = 'output/img_list.json'
with open(file_path, "w") as file:
    file.write(json_string)
print("The JSON string has been saved to a file:", file_path)

driver.quit()