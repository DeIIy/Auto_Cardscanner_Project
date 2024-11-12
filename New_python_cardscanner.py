import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

def extract_and_write_text(image_path, output_file, driver):
    max_retries = 5
    attempt = 0
    
    while attempt < max_retries:
        try:
            print(f"Attempting to process {os.path.basename(image_path)}...")
            driver.get("https://www.cardscanner.co/image-to-text")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            upload_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "image_upload"))
            )
            upload_button.send_keys(image_path)
            print("Image uploaded successfully.")

            convert_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='btn convert_files g-recaptcha d-flex align-items-center justify-content-center fs_12_sm']"))
            )
            driver.execute_script("arguments[0].click();", convert_button)
            print("Convert button clicked.")
            
            time.sleep(50)
            
            textarea = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "copyText_0"))
            )
            
            extracted_text = textarea.get_attribute('value')
            if "Error:- Uploaded Image does not contain any text" in extracted_text:
                raise Exception("Text extraction failed, error message received.")
            
            if extracted_text.strip() == '':
                raise Exception("Text extraction failed, textarea is empty.")
            
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"{extracted_text}\n")
            
            print(f"Text extracted and written to file: {os.path.basename(image_path)}")
            return
            
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt}/{max_retries} - Error occurred: {e}")
            traceback.print_exc()
            driver.refresh()
            time.sleep(5)
            print(f"Retrying {os.path.basename(image_path)}...")

    print(f"Text extraction failed after {max_retries} attempts: {os.path.basename(image_path)}")

def main_function(image_dir, output_file):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    image_paths = sorted(
        [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')],
        key=lambda x: int(re.search(r'_page-(\d+)', x).group(1)) if re.search(r'_page-(\d+)', x) else 0
    )
    
    processed_images = set()
    
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            continue
        
        if image_path in processed_images:
            print(f"Image already processed: {image_path}")
            continue
        
        extract_and_write_text(image_path, output_file, driver)
        
        processed_images.add(image_path)
        
        time.sleep(2)
        
        driver.refresh()
        time.sleep(2)

    driver.quit()

image_dir = r'C:\Users\ytetl\Image'
output_file = r'C:\Users\ytetl\extracted_texts.txt'

if not os.path.exists(r'C:\Users\ytetl'):
    os.makedirs(r'C:\Users\ytetl')

main_function(image_dir, output_file)
