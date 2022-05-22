import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from app import app,db
from app.models import User,gameRecord
import unittest

class SystemTest(unittest.TestCase):
    global driver
    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            db.init_app(app)
            db.create_all()
            u1 = User(id='00000',username='testuser1')
            u2 = User(id='11111',username='testuser2')
            u2 = User()
            db.session.add(u1)
            db.session.add(u2)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://127.0.0.1:5000/login')

    def tearDown(self) -> None:
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(gameRecord).delete()
            db.session.commit()
            db.session.remove()

    def test_register(self):
        u = User.query.get('00000')
        self.assertEqual(u.username,"testuser2",msg="testuser2 already exist in database")
        self.driver.get("http://127.0.0.1:5000/login")
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id('register').click()
        self.driver.find_element_by_id('username').send_keys('00000')
        self.driver.find_element_by_id('email').send_keys('000@000.com')
        self.driver.find_element_by_id('password').send_keys('00000')
        self.driver.find_element_by_id('password').send_keys('00000')
        time.sleep(2)
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_id('submit').click()
        self.driver.implicitly_wait(5)
        time.sleep(2)
        self.assertEqual(self.driver.find_element(By.XPATH),"/html/body/ul/ol",msg='register successfully')

if __name__ == "__main__":
    unittest.main(verbosity=2)


