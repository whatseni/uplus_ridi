# selenium webdriver
from selenium import webdriver

# selenium 키 조작
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import json
import pyperclip
import requests
import urllib.parse

driver = webdriver.Chrome()
driver.get('https://www.lguplus.com/login/fallback')
time.sleep(2)

naver_login_box = driver.find_element(By.XPATH, '//*[@id="contentsSection"]/div/div/div/div/section/ul[1]/li[2]')
naver_login_box.click()
time.sleep(2)

naver_id_box = driver.find_element(By.XPATH, '//*[@id="id"]')
naver_pw_box = driver.find_element(By.XPATH, '//*[@id="pw"]')
naver_login_button = driver.find_element(By.XPATH, '//*[@id="log.login"]')

naver_id_box.click()
pyperclip.copy("")
naver_id_box.send_keys(Keys.CONTROL, 'v')
time.sleep(2)

naver_pw_box.click()
pyperclip.copy("")
naver_pw_box.send_keys(Keys.CONTROL, 'v')
time.sleep(2)

naver_login_button.click()
time.sleep(5)

# driver cookie 딕셔너리화
_cookies = driver.get_cookies()
uplus_cookie_dict = {}
for cookie in _cookies:
    uplus_cookie_dict[cookie['name']] = cookie['value']

# 쿠키 딕셔너리의 값들을 URL 인코딩
uplus_encoded_cookie_dict = {}
for key, value in uplus_cookie_dict.items():
    if isinstance(value, str):
        uplus_encoded_cookie_dict[key] = urllib.parse.quote(value)
    else:
        uplus_encoded_cookie_dict[key] = value

uplus_session = requests.Session()

uplus_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
uplus_session.headers.update(uplus_headers)
uplus_session.cookies.update(uplus_encoded_cookie_dict)

res = uplus_session.get('https://www.lguplus.com/uhdc/fo/pogg/mypg/v1/coupon-list?cpnEposStusCd=UP&pcMblCd=P')
json_obj = json.loads(res.text)

coupon_num = json_obj['couponList'][0].get('cpnNo')
print(coupon_num)

uplus_session.close()

# 리디 셀렉트 로그인
driver.get('https://select.ridibooks.com/voucher')
ridi_login = driver.find_element(By.XPATH, '//*[@id="app"]/main/section/div/button')
ridi_login.click()
time.sleep(2)

try:
    ridi_nvr_login1 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/section/div/div/button[2]')
    ridi_nvr_login1.click()
except Exception as e:
    print("login1 element cannot find")
    driver.quit()

try:
    ridi_nvr_login2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/section/div/div[1]/button')
    ridi_nvr_login2.click()
except Exception as e:
    print("login2 element cannot find")
    driver.quit()

time.sleep(2)

# driver cookie 딕셔너리화
_cookies = driver.get_cookies()
ridi_cookie_dict = {}
for cookie in _cookies:
    ridi_cookie_dict[cookie['name']] = cookie['value']

# 리디 쿠키 딕셔너리의 값들을 URL 인코딩
ridi_encoded_cookie_dict = {}
for key, value in ridi_cookie_dict.items():
    if isinstance(value, str):
        ridi_encoded_cookie_dict[key] = urllib.parse.quote(value)
    else:
        ridi_encoded_cookie_dict[key] = value

ridi_session = requests.Session()
ridi_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
           'Content-Type': 'application/json'}
ridi_session.headers.update(ridi_headers)
ridi_session.cookies.update(ridi_encoded_cookie_dict)

req_coupon = coupon_num.replace("-", "")
req_data = {
    "voucher_code": req_coupon
}
coupon_result = ridi_session.post('https://ridibooks.com/api/select/users/me/vouchers', json=req_data)
json_coupon = json.loads(coupon_result.text)
print(json_coupon)

ridi_session.close()

# 웹 드라이버 종료
driver.quit()