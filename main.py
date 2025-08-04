from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, re

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")

print("Scan the QR code in your WhatsApp Web...")
time.sleep(20)  # wait for QR code scan

# Locate chat list
chat_list_xpath = '//div[@role="grid"]'
chat_list = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, chat_list_xpath))
)

# Scroll to load all chats
for _ in range(10):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_list)
    time.sleep(2)

chats = driver.find_elements(By.XPATH, '//div[@role="gridcell"]//span[@title]')
print(f"Found {len(chats)} chats.")

actions = ActionChains(driver)

for chat in chats:
    name = chat.get_attribute("title")

    if name and re.fullmatch(r'\+?\d+', name.replace(" ", "")):
        print(f"Deleting chat with: {name}")

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", chat)
        time.sleep(1)

        # Right-click the chat
        actions.context_click(chat).perform()

        # ✅ Wait for context menu & click Delete chat
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Delete chat")]'))
        )
        delete_button.click()
        time.sleep(1)

        # ✅ Confirm deletion by clicking the red Delete button
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Delete")]'))
        )
        confirm_button.click()
        time.sleep(2)

print("✅ Completed deleting all unsaved contact chats.")
print("Exiting...")
driver.quit()
