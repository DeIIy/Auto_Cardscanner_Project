from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui
import re

def bolumleri_al(dosya_adı):
    with open(dosya_adı, 'r', encoding='utf-8') as file:
        metin = file.read()

    noktalama = r'[.!?]'
    i = 0
    bolum_sayisi = 1

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    chrome_service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        while i < len(metin):
            bolum = metin[i:i + 800]
            son_noktalama = re.search(noktalama, bolum[::-1])
            if son_noktalama:
                son_noktalama_indeksi = len(bolum) - son_noktalama.start() - 1
                bolum = bolum[:son_noktalama_indeksi + 1]

            print(f"{bolum.strip()}\n{'-'*50}")
            print(f"Bolum {bolum_sayisi}: Metin işleniyor...")

            if bolum_sayisi == 1:
                driver.get("https://commercepro.capcut.com/editor?scenario=youtube_ads")
                print("Web sayfası açıldı.")
                time.sleep(15)

                avatar_button = WebDriverWait(driver, 480).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='workbench-tool-bar-ToolbarDigitalHuman']/div"))
                )
                avatar_button.click()
                time.sleep(3)

            script_input = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='script_input']"))
            )

            script_input.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            script_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            script_input.send_keys(bolum.strip())
            time.sleep(3)

            time.sleep(3)
            pyautogui.click(x=1777, y=686)
            time.sleep(120)

            export_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='export-video-btn']"))
            )
            export_button.click()
            time.sleep(5)

            save_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='workbench']/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/button[2]/span"))
            )
            save_button.click()
            time.sleep(5)

            name_input = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div/div[3]/form/div[1]/div[2]/div/div/div/input"))
            )

            name_input.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            name_input.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            name_input.send_keys(str(bolum_sayisi))
            time.sleep(3)

            export_final_button = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div/div[3]/div/button"))
            )
            export_final_button.click()
            time.sleep(5)

            time.sleep(75)

            driver.get("https://commercepro.capcut.com/editor/AD6BA079-37A9-4980-B63C-0CB0A42C36CA?tab_name=home&sub_tab=video&action=addDigitalHuman&__tool_type=ai_character&__tool_position=magic_tools&edit_type=ai_character&scenario=custom&scale=9%3A16&workspaceId=7436092978046697525&spaceId=7436076254833116177")
            time.sleep(15)
            pyautogui.click(x=1197, y=424)

            i += len(bolum)
            bolum_sayisi += 1

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

bolumleri_al("Metin.txt")
