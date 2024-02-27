
from selenium.webdriver.chrome.service import Service



class LicenseInformation:
    def __init__(self, chrome_driver_path):
        self.service = Service(chrome_driver_path)
        self.driver = None



    def close_browser(self):
        self.driver.quit()


# Example usage:
if __name__ == "__main__":
    chrome_driver_path = "C:/Users/DELL/Desktop/chromedriver.exe"
    license_info = LicenseInformation(chrome_driver_path)




