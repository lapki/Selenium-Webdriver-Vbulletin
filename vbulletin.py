from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
            
import time
import sys
class Vbulletin:

    def __init__(self, url, username, password, board, subject, body):
        
        self.url = url
        self.username = username
        self.password = password
        self.board = board
        self.subject = subject
        self.body = body
        self.logged_in = False

    def setup(self):

        print("Setting up")

        DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'

        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        
        self.driver.set_window_size(1120, 550)
        
    def teardown(self):

        self.driver.quit()
        print("Tearing down")

    def login(self):
        """
        Login to vbulletin account
        """

        self.driver.get(self.url)

        time.sleep(4)
                
        username = self.driver.find_element_by_name("vb_login_username")

        username.send_keys(self.username)
        try:
            password = self.driver.find_element_by_name("vb_login_password")
        
        except Exception ElementNotVisibleException:
            self.driver.execute_script("$p = document.getElementById('navbar_password'); $parent = $p.parentNode; $new = $p.cloneNode(); $new['style'].display = 'inline'; $parent.replaceChild($new, $p);")
            
            time.sleep(5)
            self.driver.execute_script("$p.click()")
            time.sleep(1)
            password.send_keys(self.password)
            
            password.submit()

        time.sleep(6)
        
        if "do=logout" in self.driver.page_source:
            print("Logged in")
            self.logged_in = True
    
    def select_board(self):
        """
        Select desired board
        """
        
        if self.logged_in == True:
            
            print("Logged in, selecting board")
            
            board = self.driver.find_element_by_link_text(self.board)
            board.click()

            print(self.driver.current_url)
            
            time.sleep(3)
            links = self.driver.find_elements_by_tag_name("a")
            new_thread = ""
            
            for link in links:
                href = link.get_attribute("href")
                if href is not None and "do=newthread" in href:
                    new_thread = href
                    #link.click()
                    break
            self.driver.get(new_thread)
            time.sleep(3)
            print(self.driver.current_url)
    
    def build_post(self):
        """
        Post fields
        
        Subject - Phread subject
        Body    - Post body
        Submit  - Submit button
        """

        print(self.driver.current_url)
        subject = self.driver.find_element_by_name("subject")
        subject.send_keys(self.subject)

        iframe = ""
        try:
            message = self.driver.find_element_by_name("message")
            message.send_keys(self.body)
            self.driver.save_screenshot("screen.png")
            message.submit()
            time.sleep(4)
        
        except Exception NoSuchElementException:
            time.sleep(3)
            
            iframe = self.driver.find_elements_by_tag_name("iframe")[3]
            #previous script had some hardcoded indices for speciic sites
            #need to rewrite this to be more general, i.e detect the relevant
            #iframe 
            
            self.driver.switch_to_frame(iframe)
            
            postbody = self.driver.find_element_by_xpath('html/body')
            
            self.driver.execute_script("text = document.createTextNode(arguments[0]); arguments[1].appendChild(text);", self.body, postbody)

            self.driver.save_screenshot("screen.png")

            self.driver.switch_to_default_content()

            print("Submitting post form")
            
            subject.submit()
            
    def main(self):
        """
        Setup webdriver
        Call automation methods
        Teardown session
        """

        self.setup()
        self.login()
        self.select_board()
        self.build_post()
        self.driver.save_screenshot('screen.png')

        print(self.driver.current_url)

        self.teardown()



#Vbulletin("url","nickname", "password","Board name","Subject","post body").main()
