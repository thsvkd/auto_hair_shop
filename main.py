import os
import json
import datetime
from typing import *
from multiprocessing.pool import ThreadPool as Pool

# from Check_Chromedriver import Check_Chromedriver
import chromedriver_autoinstaller
from termcolor import colored, cprint
import selenium
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert


class JunoHairWebCrawler:

    class SubmitChanged(object):
        def __init__(self, element, xpath):
            self.element = element
            self.xpath = xpath

        def __call__(self, driver: webdriver.Chrome):
            # here we check if this is new instance of element
            new_element = driver.find_element(By.XPATH, self.xpath)
            return new_element != self.element

    def __init__(self, headless: bool = False) -> None:
        self.driver = self.load_chrome_driver(headless)
        self.wait_driver = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(5)

    def get_user_agent(self, webdriver_path) -> str:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(
            webdriver_path, chrome_options=chrome_options)
        return driver.execute_script("return navigator.userAgent")

    def get_new_version_chrome_driver(self):
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[
            0]
        driver_path = f'./chromedriver_{chrome_ver}/chromedriver.exe'
        if os.path.exists(driver_path):
            print(f"chrom driver is insatlled: {driver_path}")
        else:
            print(f"install the chrome driver(ver: {chrome_ver})")
            chromedriver_autoinstaller.install(True)

        return driver_path

    def load_chrome_driver(self, headless: bool) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()
        # self.user_agent = self.get_user_agent(webdriver_path)
        if headless:
            chrome_options.add_argument('headless')
        # chrome_options.add_argument('window-size=500,500')
        chrome_options.add_argument(f'--window-position=2560,{1440 - 1080}')
        chrome_options.add_argument(f'--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('lang=ko_KR')
        # chrome_options.add_argument(self.user_agent)

        driver_path = self.get_new_version_chrome_driver()
        driver = webdriver.Chrome(
            driver_path, chrome_options=chrome_options)
        cprint('\ndriver load finished', 'green')
        return driver

    def switch_to_target_tab(self, window_name: str):
        try:
            self.driver.switch_to.window(window_name)
        except Exception as e:
            pass

    def implicitly_wait_off(self):
        self.driver.implicitly_wait(0)

    def implicitly_wait_on(self, timeout: int = 5):
        self.driver.implicitly_wait(timeout)

    def find_element(self, by: By, value: str):
        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str):
        return self.driver.find_elements(by, value)

    def wait_find_element(self, by: By, value: str):
        return self.wait_driver.until(EC.element_to_be_clickable((by, value)))

    def get_site(self, url, tab_name):
        self.driver.get(url)
        self.switch_to_target_tab(tab_name)

    def login(self, id, password):
        self.driver.find_element(
            by=By.XPATH, value='/html/body/div/div[3]/div[2]/div/div[2]/div/a[1]').click()
        login_textbox_ID = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/div/div/div[2]/form/div/div[1]/div[1]/p[1]/input')
        login_textbox_PASSWORD = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/div/div/div[2]/form/div/div[1]/div[1]/p[2]/input')
        login_button = self.driver.find_element(
            by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/div/div/div[2]/form/div/div[1]/div[2]/a')

        login_textbox_ID.click()
        login_textbox_ID.send_keys(id)

        login_textbox_PASSWORD.click()
        login_textbox_PASSWORD.send_keys(password)

        login_button.click()

    def select_city(self, select_city: str):
        flag = False

        self.driver.find_element(
            By.XPATH, '/html/body/div/div[3]/div[2]/div[3]/div/ul/li[1]/strong/a').click()
        locate_list: List[WebElement] = self.driver.find_element(
            by=By.XPATH, value='/html/body/div/div[3]/div[2]/div[3]/div/ul/li[1]/div/ul').find_elements(By.TAG_NAME, 'li')[1:]
        for i, locate_element in enumerate(locate_list):
            city_name = locate_element.text
            j = i + 1
            print(f'{j:<3}: {city_name}')

            if city_name == select_city:
                flag = j

        if flag:
            locate_list[flag-1].click()
            print('선택한 시 : ', select_city)
        else:
            user_sel = int(input('어느 시? : '))
            locate_list[user_sel-1].click()

    def select_section(self, select_section: str):
        flag = False

        self.driver.find_element(
            By.XPATH, '/html/body/div/div[3]/div[2]/div[3]/div/ul/li[2]/strong/a').click()
        locate_list: List[WebElement] = self.driver.find_element(
            by=By.XPATH, value='/html/body/div/div[3]/div[2]/div[3]/div/ul/li[2]/div/ul').find_elements(By.TAG_NAME, 'li')[1:]
        for i, locate_element in enumerate(locate_list):
            section_name = locate_element.text
            j = i + 1
            print(f'{j:<3}: {section_name}')

            if section_name == select_section:
                flag = j

        if flag:
            locate_list[flag-1].click()
            print('선택한 구 : ', select_section)
        else:
            user_sel = int(input('어느 구? : '))
            locate_list[user_sel-1].click()

    def select_store(self, select_store: str):
        flag = False

        store_list: List[WebElement] = self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[3]/div[2]/div[5]/div/div/div[1]'))).find_elements(By.CLASS_NAME, 'shop_item')

        try:
            for i, store_element in enumerate(store_list):
                store_name = store_element.find_element(By.CLASS_NAME,
                                                        'si_info_inner').find_element(By.TAG_NAME, 'strong').text
                j = i + 1
                print(f'{j:<3}: {store_name}')

                if store_name == select_store:
                    flag = j
            if flag:
                store_list[flag-1].click()
                print('선택한 매장 : ', select_store)
            else:
                user_sel = int(input('어느 매장? : '))
                store_list[user_sel-1].click()

            return True
        except Exception:
            if self.wait_driver.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[2]/div[5]/div/div/div[1]/div'))).text.strip() == '데이터 없음':
                print('매장이 존재하지 않습니다... 다시 선택해주세요.')
            else:
                print('뭔가 이상하다..!')

            return False

    def select_designer(self, select_designer: str):
        flag = False

        # recommend_designer
        self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/ul/li[1]/a/span'))).click()

        # hair_length_radio
        self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div[2]/div/div[3]/div/div/div/span[1]/input').click()

        # hair_cut_radio
        self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div[2]/div/div[4]/div/div/div/span[3]/input').click()

        # select_fin_button
        self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div[3]/div/div[2]/a').click()

        designer_list = self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div/ul'))).find_elements(By.TAG_NAME, 'li')

        for i, designer_element in enumerate(designer_list):
            designer_name = designer_element.find_element(
                By.CLASS_NAME, 'ttl').text
            designer_desc = designer_element.find_element(
                By.CLASS_NAME, 'desc').text

            j = i + 1
            print(f'{j:<3}: {designer_name}')

            if designer_name == select_designer:
                flag = j

        if flag:
            designer_list[flag-1].click()
            print('선택한 매장 : ', select_designer)
        else:
            user_sel = int(input('헤어다자이너를 선택하세요 : '))
            designer_list[user_sel-1].click()

    def select_date(self, select_date: str):
        today = datetime.date.today()
        if select_date:
            select_date = select_date.split('-')
            target_year = select_date[0]
            target_month = select_date[1]
            target_day = select_date[2]
        else:
            while True:
                user_sel = input(
                    f'예약할 날짜를 선택하세요 ({today.month}월 {today.day}일 이후로만, ex: 5-23 or 05-23 or 2022-05-12): ')
                user_sel = user_sel.split('-')
                if len(user_sel) == 3:
                    target_year = user_sel[0]
                    target_month = user_sel[1]
                    target_day = user_sel[2]
                elif len(user_sel) == 2:
                    target_year = today.year
                    target_month = user_sel[0]
                    target_day = user_sel[1]
                elif len(user_sel) == 1:
                    target_year = today.year
                    target_month = today.month
                    target_day = user_sel[0]
                else:
                    print('잘못된 입력입니다. ')
                    continue
                break

        while True:
            calendar = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[1]')

            date_raw_list = calendar.find_element(
                By.ID, 'caltbody').find_elements(By.TAG_NAME, 'tr')
            date_list: List[WebElement] = []

            self.implicitly_wait_off()
            for date_raw_element in date_raw_list:
                date_raw_element_list = date_raw_element.find_elements(
                    By.TAG_NAME, 'td')
                for date_element in date_raw_element_list:
                    try:
                        if date_element.find_element(By.TAG_NAME, 'a'):
                            date_list.append((date_element.text, date_element))
                    except Exception:
                        continue
            self.implicitly_wait_on(5)

            month_left_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/a[1]')
            month_right_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/a[2]')

            calendar_head = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[1]/div[1]/span')
            dis_year = calendar_head.text.split('.')[0]
            dis_month = calendar_head.text.split('.')[1]

            if int(target_year) == int(dis_year) and int(target_month) == int(dis_month):
                for date_element in date_list:
                    if date_element[0] == target_day:
                        date_element[1].click()
                        break
                break
            else:
                year_gap = int(target_year) - int(dis_year)
                month_gap = int(target_month) - int(dis_month)
                total_month_gap = year_gap * 12 + month_gap

                if total_month_gap < 0:
                    for _ in range(abs(total_month_gap)):
                        month_left_button.click()
                        self.wait_driver.until(
                            EC.element_to_be_clickable(month_left_button))
                else:
                    for _ in range(abs(total_month_gap)):
                        month_right_button.click()
                        self.wait_driver.until(
                            EC.element_to_be_clickable(month_right_button))

    def select_time(self, select_time: str):
        time_selection_box = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[2]')

        am_time_list = self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div[3]/div[1]/ul'))).find_elements(By.TAG_NAME, 'li')
        pm_time_list = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div[3]/div[2]/ul').find_elements(By.TAG_NAME, 'li')

        self.implicitly_wait_off()
        whole_time_list: List[WebElement] = []
        for time_element in am_time_list:
            try:
                if time_element.find_element(By.TAG_NAME, 'a'):
                    whole_time_list.append(time_element)
            except Exception:
                pass

        for time_element in pm_time_list:
            try:
                if time_element.find_element(By.TAG_NAME, 'a'):
                    whole_time_list.append(time_element)
            except Exception:
                pass
        self.implicitly_wait_on()

        now = datetime.datetime.now()

        if select_time:
            select_time = select_time.split(':')
            target_hour = select_time[0]
            target_minute = select_time[1]

            for time_element in whole_time_list:
                if time_element.text == f'{target_hour}:{target_minute}':
                    time_element.click()
                    return
            else:
                print(
                    f'해당 시간 ({target_hour}:{target_minute})은 예약이 불가능합니다. 다른 시간을 선택해주세요')

        for i, time_element in enumerate(whole_time_list):
            j = i + 1
            print(f'{j:<3}: {time_element.text}')

        if len(whole_time_list) > 0:
            user_sel = input(
                f'예약할 시간을 선택하세요 ({now.hour}시 {now.minute}분 이후로만, ex: 6:30): ')

            user_sel = int(user_sel) - 1
            whole_time_list[user_sel].click()

            return True
        else:
            print('예약 가능 시간이 없습니다... 다른 날짜를 선택해주세요.')
            return False

    def reservation(self, reservation_info: dict):
        self.driver.find_element(
            by=By.XPATH, value='/html/body/div/div[3]/div[2]/div/div[1]/div[1]/a').click()

        while True:
            self.select_city(reservation_info['city'])
            self.select_section(reservation_info['section'])
            ret = self.select_store(reservation_info['store'])

            if ret:
                break

        self.select_designer(reservation_info['designer'])

        while True:
            self.select_date(reservation_info['date'])
            ret = self.select_time(reservation_info['time'])

            if ret:
                break

        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[5]/div/ul/li[3]/a').click()
        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[6]/ul/li[1]/span/input').click()
        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[10]/a[2]').click()

        self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[3]/div[2]/div[3]/div[3]/span/label'))).click()
        self.driver.find_element(
            By.XPATH, '/html/body/div/div[3]/div[2]/div[3]/div[4]/a[2]').click()

        res_finish_msg = self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[3]/div[2]/div/p[1]'))).text
        if '예약이 완료되었습니다' in res_finish_msg:
            print('예약 완료')

    # TODO: complete this!!!
    def reservation_cancel(self, reservation_cancel_info: dict):
        # go to 이용내역
        self.driver.find_element(
            By.XPATH, '/html/body/div/div[1]/div[1]/div[1]/div/ul/li[5]/a').click()
        self.driver.find_element(
            By.XPATH, '/html/body/div/div[3]/div[2]/div/ul/li[2]/strong/a').click()

        # get 이용 내역 리스트
        res_list_box = self.wait_driver.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[3]/div[4]/div/div/div[2]/div/table/tbody')))
        res_raw_list = [
            element for element in res_list_box.find_elements(By.TAG_NAME, 'tr')]
        res_cancel_button_list: List[WebElement] = []
        i = 0
        for res_button in res_raw_list:
            date_element = res_button.find_elements(By.TAG_NAME, 'td')[0]
            info_elements = res_button.find_elements(By.TAG_NAME, 'td')[
                1].find_elements(By.TAG_NAME, 'p')
            price_element = res_button.find_elements(By.TAG_NAME, 'td')[2]
            button_element = res_button.find_elements(By.TAG_NAME, 'td')[3]

            today = datetime.date.today()
            res_date = date_element.text.split('-')
            res_date = datetime.date(
                int(res_date[0]), int(res_date[1]), int(res_date[2]))

            if today <= res_date:
                button_span_element = button_element.find_element(
                    By.TAG_NAME, 'span')
                if button_span_element:
                    if button_span_element.text == '완료':
                        print(
                            f'{i+1:<3}: {date_element.text}, {info_elements[0].text}|{info_elements[1].text} 예약완료')
                        res_cancel_button_list.append(
                            button_element.find_element(By.TAG_NAME, 'a'))
                        i += 1
                    elif button_span_element.text == '예약취소':
                        # print(f'\" {td_element[0].text} 예약취소')
                        pass
                else:
                    # print(f'\" {td_element[0].text} 이용완료')
                    pass

        if len(res_cancel_button_list) == 0:
            print('취소할 예약 내역이 없습니다...')
            return
        else:
            user_res_cancel = int(input('어떤 예약을 취소하시겠습니까? : '))
            res_cancel_button_list[user_res_cancel-1].click()
            alert_text = Alert(self.driver).text
            Alert(self.driver).accept()

            # self.implicitly_wait_on()
            # if res_button.find_elements(By.TAG_NAME, 'td')[3].find_element(By.TAG_NAME, 'span').text == '예약취소':
            #     print('예약 취소 완료!')
            # else:
            #     print('예약 취소 실패...')

    def run(self):
        self.get_site(
            'https://www.junohair.com/junohair/reservation/intro', '준오헤어')

        self.login('ID', 'PASSWORD')

        try:
            with open('config.json', 'r', encoding="UTF-8") as file:
                data = json.load(file)
            user_select = data['reservation']
            if user_select == 0:
                print('예약 모드로 작동...')
            else:
                print('예약 취소 모드로 작동...')
        except FileNotFoundError:
            while True:
                user_select = input('예약(0)? 예약 취소(1)? : ')
                if user_select == '0' or user_select == '1':
                    user_select = int(user_select)
                    break
                else:
                    print('0, 1 중 하나만 입력해주세요')

            data = {
                "reservation": None,
                "city": None,
                "section": None,
                "store": None,
                "designer": None,
                "date": None,
                "time": None
            }

        if user_select == 0:
            self.reservation(data)
        elif user_select == 1:
            self.reservation_cancel(data)


if __name__ == '__main__':
    juno_web_crwler = JunoHairWebCrawler(headless=False)
    try:
        juno_web_crwler.run()
    except KeyboardInterrupt:
        print('exit program...')
