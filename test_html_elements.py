from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestTasks(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_tasks_display(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(2)
        self.assertIn("Task", driver.page_source)

        task_rows = driver.find_elements(By.XPATH, "//table//tr")
        self.assertGreater(len(task_rows), 1, "No tasks found in the table")

    def test_add_task(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(2)

        desc_input = driver.find_element(By.NAME, "description")
        desc_input.send_keys("Test Task")

        status_dropdown = driver.find_element(By.NAME, "status")
        for option in status_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.text == "Pending":
                option.click()
                break

        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

        time.sleep(2)
        self.assertIn("Test Task", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
