from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, re

# Configure Chrome
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

# Scroll multiple times to load all chats
for _ in range(10):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_list)
    time.sleep(2)

# Fetch chat titles (contact names or numbers)
chats = driver.find_elements(By.XPATH, '//div[@role="gridcell"]//span[@title]')
print(f"Found {len(chats)} chats.")

for chat in chats:
    name = chat.get_attribute("title")

    # Check if chat is a phone number (unsaved contact)
    if name and re.fullmatch(r'\+?\d+', name.replace(" ", "")):
        print(f"Deleting chat with: {name}")

        # Scroll into view & click using JS
        driver.execute_script("arguments[0].scrollIntoView(true);", chat)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", chat)

        # ✅ Wait for chat header (user info at top) to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//header'))
        )
        time.sleep(1)

        # ✅ Try multiple menu button selectors
        menu_selectors = [
            '//div[@role="button" and @aria-label="Menu"]',
            '//span[@data-icon="menu"]'
        ]

        menu_button = None
        for selector in menu_selectors:
            try:
                menu_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                break
            except:
                continue

        if not menu_button:
            print(f"⚠️ Menu button not found for {name}, skipping.")
            continue

        menu_button.click()
        time.sleep(1)

        # ✅ Click "Delete chat"
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Delete chat"]'))
        )
        delete_button.click()
        time.sleep(1)

        # ✅ Confirm deletion
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="DELETE CHAT"]'))
        )
        confirm_button.click()
        time.sleep(2)

print("✅ Completed deleting all unsaved contact chats.")
driver.quit()
