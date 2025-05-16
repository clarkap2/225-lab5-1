from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time
import os

class TestShoppingList(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.base_url = os.getenv("TEST_URL", "http://localhost:5000")

    def test_items_display(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)
        self.assertIn("Shopping", driver.page_source)

    def test_add_item(self):
        driver = self.driver
        driver.get(self.base_url)
        time.sleep(2)

        input_box = driver.find_element(By.NAME, "item")
        input_box.send_keys("Milk")

        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Add Item']")
        submit_button.click()

        time.sleep(2)
        self.assertIn("Milk", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
