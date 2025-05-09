import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from lib.logger import get_logger


log = get_logger()

class BrowserManager:
    def __init__(self, wait_time=5):
        self.wait_time = wait_time
        self.driver = None
        self.wait = None
        
    def __enter__(self):
        # 크롬 드라이버 옵션 설정
        options = webdriver.ChromeOptions()
        
        options.add_argument('--headless')
        options.add_argument('--no-zygote')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--window-size=1920x1080')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')

        chrome_path = os.environ.get('CHROME_BIN', None)
        if chrome_path:
            options.binary_location = chrome_path

        try:
            driver_path = os.environ.get('CHROMEDRIVER_PATH', None)
            if driver_path:
                # 도커 환경일 경우
                self.driver = webdriver.Chrome(
                    service=Service(driver_path),
                    options=options
                )
            else:
                # 도커 환경이 아닐 경우
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )
            self.wait = WebDriverWait(self.driver, self.wait_time)
            return self.driver, self.wait
        except Exception as e:
            log.error(f"드라이버 초기화 중 오류 발생: {str(e)}")
            raise
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                log.error(f"브라우저 종료 중 오류 발생: {str(e)}") 