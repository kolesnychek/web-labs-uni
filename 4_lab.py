import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_data_from_endpoint():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    if response.status_code == 200:
        return response.json()
    return None

class TestAPI(unittest.TestCase):
    def test_endpoint_response(self):
        data = get_data_from_endpoint()
        self.assertIsNotNone(data)
        self.assertIn("title", data)

    def test_complex_scenario(self):
        data = get_data_from_endpoint()
        if data:
            new_response = requests.post("https://jsonplaceholder.typicode.com/posts", json={"title": data["title"]})
            self.assertEqual(new_response.status_code, 201)

class TestPerformance(unittest.TestCase):
    def test_response_time(self):
        start_time = time.time()
        get_data_from_endpoint()
        end_time = time.time()
        self.assertTrue(end_time - start_time < 2, "Response time too slow!")

class TestScraping(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")

    def test_scrape_data(self):
        driver = self.driver
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        submit = driver.find_element(By.NAME, "submit")
        
        username.send_keys("testuser")
        password.send_keys("testpassword")
        submit.send_keys(Keys.RETURN)
        time.sleep(3)
        
        data_element = driver.find_element(By.ID, "data-container")
        self.assertIsNotNone(data_element.text)
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
