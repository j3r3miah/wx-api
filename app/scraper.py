import json
import logging

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

log = logging.getLogger(__name__)


class Scraper:
    """ Wind spot scraper """

    def __init__(
        self,
        chrome_webdriver_path,
        data_path,
        website_urls
    ):
        self.driver = webdriver.Chrome(executable_path=chrome_webdriver_path)
        self.driver.implicitly_wait(2)
        self.data_path = data_path
        self.urls = website_urls

    def shutdown(self):
        self.driver.quit()

    def login(self, username, password, retries=1):
        log.info('attemping login')
        self.driver.get(self.urls['login'])
        if self._try_load_cookies():
            self.driver.refresh()
            if self._islogged_in():
                log.info('resumed session')
                return True
        log.info('logging in')
        success = self._login(username, password)
        if success:
            self._configure_session()
            self._save_cookies()
        return success

    def get_spot_data(self, spot_id):
        log.info('retrieving spot data: %d' % spot_id)
        self.driver.get(self.urls['spot'] % spot_id)

        title = self.driver.find_element_by_id('spot-info-title').text
        date = self.driver.find_element_by_class_name('jw-cc-data-date').text
        speed = self.driver.find_element_by_class_name('jw-cc-data-speed').text
        gust = (
            self.driver.find_element_by_css_selector(
                "div[class='jw-data-gust jw-data-item']"
            ).text
        )
        air_temp = (
            self.driver.find_element_by_css_selector(
                "div[class='jw-data-air-temp jw-data-item']"
            ).text
        )
        air_pressure = (
            self.driver.find_element_by_css_selector(
                "div[class='jw-data-air-pressure jw-data-item']"
            ).text
        )

        e = self.driver.find_element_by_class_name('jw-cc-data-gauge')
        # TODO: screenshot page and crop to above element dimensions

        return {
            'title': title,
            'date': date,
            'wind_speed': speed,
            'wind_gust': gust,
            'air_temp': air_temp,
            'air_pressure': air_pressure,
        }

    @property
    def _cookie_path(self):
        return '{}/cookies.json'.format(self.data_path)

    def _save_cookies(self):
        json.dump(self.driver.get_cookies(), open(self._cookie_path, 'w'))

    def _try_load_cookies(self):
        # a page in same domain as cookies must first be loaded
        try:
            d = json.load(open(self._cookie_path))
        except:
            return False
        for cookie in d:
            self.driver.add_cookie(cookie)
        return True

    def _islogged_in(self):
        # this assumes that a page which includes user account nav is visible
        try:
            WebDriverWait(self.driver, 2).until(
                lambda driver: driver.find_element_by_class_name('signed-in')
            )
            return True
        except:
            return False

    def _login(self, username, password, retries=1):
        # this assumes `self.urls['login']` is already loaded
        uname = self.driver.find_element_by_name('isun')
        uname.send_keys(username)
        passw = self.driver.find_element_by_name('ispw')
        passw.send_keys(password)
        submit_button = self.driver.find_element_by_name('iwok.x')
        submit_button.click()
        if self._islogged_in():
            return True
        if retries > 0:
            # it takes two tries for login to succeed, oddly
            self.driver.get(self.urls['login'])
            return self._login(username, password, retries - 1)
        return False

    def _configure_session(self):
        """ Assumes at least one cookie exists already """

        # goofy... idea is to keep domain string out of source control ;)
        domain = self.driver.get_cookies()[0]['domain']
        self.driver.add_cookie(
            {'domain': domain,
             'expiry': 2368505078,
             'httpOnly': False,
             'name': 'TemperatureUnits',
             'path': '/',
             'secure': False,
             'value': 'f'}
        )
        self.driver.add_cookie(
            {'domain': domain,
             'expiry': 2368505081,
             'httpOnly': False,
             'name': 'DistanceUnits',
             'path': '/',
             'secure': False,
             'value': 'mi'}
        )
        self.driver.add_cookie(
            {'domain': domain,
             'expiry': 2368505074,
             'httpOnly': False,
             'name': 'SpeedUnits',
             'path': '/',
             'secure': False,
             'value': 'kts'}
        )
        self.driver.add_cookie(
            {'domain': domain,
             'expiry': 2368505090,
             'httpOnly': False,
             'name': 'cad',
             'path': '/',
             'secure': False,
             'value': '0'}
        )
