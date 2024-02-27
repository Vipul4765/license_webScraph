import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import base64
from io import BytesIO


class LicenseInformation:
    def __init__(self, chrome_driver_path):
        self.service = Service(chrome_driver_path)
        self.driver = None

    def open_browser(self, url):
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(url)

    def input_license_number(self, license_number):
        try:
            license_input = self.driver.find_element(By.XPATH, '//*[@id="form_rcdl:tf_dlNO"]')
            license_input.send_keys(license_number)
        except WebDriverException as e:
            print(f"An error occurred while entering license number: {e}")
            raise

    def input_date_of_birth(self, date_of_birth):
        try:
            date_input_field = self.driver.find_element(By.ID, "form_rcdl:tf_dob_input")
            date_input_field.click()
            wait = WebDriverWait(self.driver, 10)
            calendar_popup = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-datepicker-calendar")))
            set_date_script = f"arguments[0].value='{date_of_birth}';"
            self.driver.execute_script(set_date_script, date_input_field)
            self.driver.execute_script("arguments[0].onchange();", date_input_field)
        except WebDriverException as e:
            print(f"An error occurred while entering date of birth: {e}")
            raise

    def capture_and_save_captcha_image(self, xpath, save_path):
        try:
            img_base64 = self.driver.execute_script("""
                var ele = arguments[0];
                var cnv = document.createElement('canvas');
                cnv.width = ele.width; cnv.height = ele.height;
                cnv.getContext('2d').drawImage(ele, 0, 0);
                return cnv.toDataURL('image/jpeg').substring(22);    
                """, self.driver.find_element(By.XPATH, xpath))

            image_data = base64.b64decode(img_base64)
            image = Image.open(BytesIO(image_data))

            # Save the image
            image.save(save_path)

            # Display the image
            image.show()

        except WebDriverException as e:
            print(f"An error occurred while capturing and saving captcha image: {e}")
            raise

    def input_captcha(self, captcha):
        try:
            captcha_input = self.driver.find_element(By.XPATH, '//*[@id="form_rcdl:j_idt39:CaptchaID"]')
            captcha_input.send_keys(captcha)
        except WebDriverException as e:
            print(f"An error occurred while entering captcha: {e}")
            raise

    def submit(self):
        self.driver.find_element(By.XPATH,'//*[@id="form_rcdl:j_idt50"]').click()

    def wait_for_redirect(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_changes(self.driver.current_url))
        except TimeoutException:
            print("Timeout waiting for redirect")

    def html_convert(self):
        # Wait for redirect to complete
        self.wait_for_redirect()

        # Capture and save HTML
        html = self.driver.page_source
        with open('info.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def close_browser(self):
        self.driver.quit()


# Example usage:
if __name__ == "__main__":
    chrome_driver_path = "C:/Users/DELL/Desktop/chromedriver.exe"
    license_info = LicenseInformation(chrome_driver_path)

    try:
        license_info.open_browser("https://parivahan.gov.in/rcdlstatus/?pur_cd=101")
        license_info.input_license_number('UP-1720230001287')
        license_info.input_date_of_birth("25-12-2002")
        try:
            license_info.capture_and_save_captcha_image('//*[@id="form_rcdl:j_idt39:j_idt44"]', "captcha_image.jpg")
        except TimeoutException:
            print("No DL found")
            exit()

        captcha = input('Enter Captcha: ')
        license_info.input_captcha(captcha)
        license_info.submit()
        license_info.html_convert()



    finally:
        time.sleep(3000)
        license_info.close_browser()

    time.sleep(300)

