from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import urllib.parse
import os
from dotenv import load_dotenv



available_numbers = {
    '9653148792':'kaanchan',
    '8450995752':'Abhiraj singh rajpurohit',
    '8828296303':'karan shelar',
    '7620967264':'dimple rajpurohit',
    '8094935507':'ishwar singh rajpurohit'}

load_dotenv()

def send_whatsapp_messages( phone_number, message,country_code="91"):

    headless = str(os.getenv('HEADLESS', 'True')).lower() in ['true', '1', 'yes']
    print(headless)
        
    driver = None
    try:

        profile_dir = os.path.join(os.getcwd(), "chrome_profile")
        os.makedirs(profile_dir, exist_ok=True)
        if len(phone_number) != 10:
            return 'context: tell user to provide a valid phone number'
        full_phone = f"{country_code}{phone_number}"
        encoded_message = urllib.parse.quote(message)
        
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,720")
        
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        
        service = Service()
        
        print("Starting Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        wa_url = f"https://web.whatsapp.com/send?phone={full_phone}&text={encoded_message}"
        print(f"Opening WhatsApp Web for {full_phone}...")
        driver.get(wa_url)
        
        try:
            qr_code_wait = WebDriverWait(driver, 5)
            qr_code = qr_code_wait.until(
                EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
            )
            
            if headless:
                print("\n*** SESSION EXPIRED - QR CODE NEEDS SCANNING ***")
                print("Please run the script again with headless=False to scan the QR code.")
                print("Example: send_whatsapp_message(country_code, phone_number, message, headless=False)")
                driver.quit()
                return False
            else:
                print("\nPlease scan the QR code with your WhatsApp app.")
                print("Waiting for scan...")
                WebDriverWait(driver, 120).until(
                    EC.invisibility_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
                )
                print("QR code scanned successfully!")
        except TimeoutException:
            pass
        
        print("Waiting for WhatsApp Web to load...")
        send_button_xpath = '//button[@aria-label="Send"]'
        wait = WebDriverWait(driver, 60)
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        
        time.sleep(2) 
        send_button.click()
        time.sleep(3)

        print("Message sent successfully!")
        
        time.sleep(2)
        driver.quit()
        return True

        
    except TimeoutException:
        if headless:
            print("\n*** SESSION MAY HAVE EXPIRED ***")
            print("Failed to load WhatsApp Web or send button not found.")
            print("Please run the script again with headless=False to check if you need to scan the QR code.")
            print("Example: send_whatsapp_message(country_code, phone_number, message, headless=False)")
        else:
            print("\nFailed to load WhatsApp Web or send button not found.")
            print("Please check your internet connection and try again.")
        
        if driver:
            driver.quit()
        return False
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False

