import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
import time
import cv2
import numpy as np
import requests
from uuid import uuid4
from tqdm import tqdm
import os


def download_img(url, save_dir):
    r = requests.get(url).content
    image = np.frombuffer(r, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # image = cv2.resize(image, (1024, 1024)) #resize 1024*1024
    cv2.imwrite(f'{save_dir}/{uuid4()}.png', image)


# # _aacl _aaco _aacw _aacx _aad7 _aade
# follow_list = []
# browser.get(f'{url}/zu00423828/following/')
# # WebDriverWait(browser, 15).until(
# #     EC.presence_of_element_located((By.XPATH, "//div[@class='_aacl _aacp _aacu _aacx _aad6 _aade']")))
# WebDriverWait(browser, 15).until(
#     EC.presence_of_element_located((By.XPATH,  "//span[@class='_aap6 _aap7 _aap8']")))
# # time.sleep(15)
# follow_button = browser.find_elements(
#     By.XPATH, "//div[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")
# print(len(follow_button))
# for i, button in enumerate(follow_button):
#     print(i, button.text)
#     # if i == 2:
#     #     button.click()
#     #     print(browser.current_url)

def get_ig_image(channel):
    img_list = []
    save_dir = f"test/{channel}"
    if os.path.exists(save_dir):
        return
    os.makedirs(save_dir, exist_ok=True)
    browser.get(f"https://instagram.com/{channel}")
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_aagv')))
    try:
        WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='_aacl _aaco _aacw _aad3 _aad6 _aadb']")))
    except Exception as e:
        print(e)
    button = browser.find_element(
        By.XPATH, "//div[@class='_aacl _aaco _aacw _aad3 _aad6 _aadb']")
    # print(button)
    if button != None:
        button.click()
    while len(img_list) < 50:
        soup = Soup(browser.page_source, "lxml")
        results = soup.find_all(class_="_aagv")
        for result in tqdm(results):
            img_url = result.img.get("src")
            if img_url in img_list:
                continue
            img_list.append(img_url)
            download_img(img_url, save_dir)
        time.sleep(5)
        browser.execute_script('window.scrollBy(0,500)')
    # browser.close()


def browser_init():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(
        "/home/yuan/桌面/tempcode/crawler_ettody/chromedriver", options=options)
    url = "https://www.instagram.com"
    browser.get(url)
    with open("cookies.json", 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()
    return browser


if __name__ == "__main__":
    ig_channels = ["applemei0914", "mk_xup", "8841jessie", "yuri_live_0411", "jaly_chan", "senyeyezi", "__tingwong",
                   "angel20739", "niya840325", "a227795", "lintsuki", "firefly880605", "miao11255", "yuniko0720", "54jojo1208",
                   "lois06277", "berylovee", "u.710", "juliamisakii", "et.1231", "estherx118", "dollshin", "1989ivyshao", "ilove7388",
                   "alephant_0427", "uccu0323"]
    browser = browser_init()
    for ig_channel in ig_channels:
        print(ig_channel)
        get_ig_image(ig_channel)
        time.sleep(10)
    browser.quit()
