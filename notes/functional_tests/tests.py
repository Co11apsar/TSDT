from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser =webdriver. Chrome()
    def tearDown (self):
        self.browser.quit()
    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table=self.browser.find_element(By.ID,'id_list_table')
                rows=table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_and_retrieve_it_later(self):
    #张三听说有—个在线待办事工项的应用
    #他去看了这个应用的首页
        self.browser.get(self.live_server_url)#(1)他注意到网页的标题和头部都包含“To-Do"这个词
        self.assertIn( 'To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text 
        self.assertIn( 'To-Do', header_text)
    #应用有—个输入待办事I项的文本输入框
        inputbox = self.browser.find_element(By.ID,'id_new_item') #(1)
        self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Enter a to-do item'
        )
        #他在文本输入框中输入了“Buy flowers""
        inputbox.send_keys( 'Buy flowers')#(2)
        #他按了回年每建钱建建后,页面更新了
        #待办事项表格中显示了“1:Buy flowers"
        inputbox.send_keys(Keys.ENTER)#(3)time-sleep(1)#(4)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: Buy flowers')
        
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')

        self.fail('Finish the test!')
        #页面再次更新,她的清单中显示了这两个待办事项

