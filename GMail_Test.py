'''
Project: GMailTest Automation
Author: Mahesh

Requirements : Selenium , selniumbase or undetected_chromedriver

Description: In This Project the tasks has to be perfomed on GMail which is a major mail service provider by Google, Inc.

Generally , GMail will not encourage any kind of automation to prevent bots in raelworld.
Inorder to bypass Automation Detectors , we need to use Selenium Webdriver in stealth mode for that seleniumbase and undetected_chromedriver are best suited options.

Inorder to make this script working , Replace the username and password. Create and use app_password from Google Account.

If It Prompts For 2FA please complete it , Added 20sec Sleep time to complete it

For Test Cases , All Asserts are followed with a successs print messages as assert will print message andterminate the program if condition fails.

For Security Reasons all the credentials has been removed. 

Perfoming automation with some of the google based products is always challenging as they always try to block or prevent bot environments.

'''








from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as us
import unittest
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import ElementNotInteractableException
from seleniumbase import Driver
import imaplib
import email

class GMailTest(unittest.TestCase):
    
    #Add Email id between quotes
    username =""
    #Add The  password 
    password = ''
    #Add App password generated on Google Account can be generated @ https://myaccount.google.com/apppasswords
    app_password =""
    
    
    @classmethod
    def setUpClass(cls):
        cls.driver = Driver(uc=True, incognito=True)
    
    #First Test will login to gmail follow up if any 2FA Asked 
    def test_gmailLogin(self):
        try:
            self.driver.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
            wait = WebDriverWait(self.driver, 15)
            email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
            email_field.send_keys(self.username)
            email_field.send_keys(Keys.ENTER)
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(20)
        except TimeoutException:
            print("Timed Out ... Try Again....")
    
    
    #send mail with Social lable , Subjest and given msg body
    def test_sendMail(self):
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Compose']")))
        compose_button = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Compose']")
        compose_button.click()
        to_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='agP aFw']")))
        to_field.send_keys("jonnyafroz@gmail.com")
        subject_field = self.driver.find_element(By.NAME, "subjectbox")
        subject_field.send_keys("Test Mail")
        body_field = self.driver.find_element(By.XPATH, "//div[@aria-label='Message Body']")
        body_field.send_keys("Test Email Body")
        more_options = self.driver.find_element(By.XPATH, "//div[@aria-label='More options']")
        more_options.click()
        label_option = self.driver.find_element(By.XPATH, "//div[text()='Label']")
        label_option.click()
        social_label =  wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='bqf']")))
        social_label.send_keys('Social'+Keys.ENTER)
        send_button = wait.until(EC.presence_of_element_located((By.XPATH,  "//div[@class='dC']/div[1]")))    
        send_button.click()
        time.sleep(5)
        
        self.driver.find_element(By.XPATH, "//input[@class='gb_xe aJh']").send_keys("category:social"+Keys.ENTER)
        time.sleep(5)
        path_i = "//img[@class='T-KT-JX']"
        req_img = self.driver.find_element(By.XPATH,path_i)
        
        assert req_img is not None, "Mail isn't Labled Correctly as Social"
        print("Validated!..Mail Labled as Social")
            
        self.validate_GMAIL()
        
        '''
        button_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='bqe' and text()='Test Mail']")))
        try:
            button_element.click()
            time.sleep(3)
        except ElementNotInteractableException:        
            self.driver.execute_script("arguments[0].scrollIntoView();", button_element)
        time.sleep(10)
        '''
    #validate the recieved mail with imaplib with gmail host
    def validate_GMAIL(self):
        gmail_host= 'imap.gmail.com'
        mail = imaplib.IMAP4_SSL(gmail_host)
        mail.login(self.username, self.app_password)
        mail.select("INBOX")
        _, selected_mails = mail.search(None,'(FROM "jonnyafroz@gmail.com")')
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data)
            
            assert email_message["subject"] == 'Test Mail', "Incorrect Mail Subject Validate"
            print("Validated..! Subject is Test Mail")
            
        for part in email_message.walk():
            if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                message = part.get_payload(decode=True)
                assert message.decode() =='Test Mail Body' , "Incorrect Mail Body"
                print("Validated..! Message Body is Test Mail Body")
            
    
        
    #Tear down the setup to close the driver opened 
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    
    

if __name__ == "__main__":
    unittest.main(warnings='ignore')