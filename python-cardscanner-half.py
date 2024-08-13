import os
from PIL import Image
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def split_image(image_path, output_dir):
    img = Image.open(image_path)
    width, height = img.size
    left = img.crop((0, 0, width // 2, height))
    right = img.crop((width // 2, 0, width, height))
    
    base_name = os.path.basename(image_path).replace('.jpg', '')
    left_path = os.path.join(output_dir, f"{base_name}_left.jpg")
    right_path = os.path.join(output_dir, f"{base_name}_right.jpg")
    
    left.save(left_path)
    right.save(right_path)
    
    return left_path, right_path

def extract_and_write_text(image_path, output_file, driver):
    max_retries = 3
    attempt = 0
    
    while attempt < max_retries:
        try:
            driver.get("https://www.cardscanner.co/image-to-text")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            upload_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "image_upload"))
            )
            upload_button.send_keys(image_path)
            
            convert_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='d-flex align-items-center justify-content-center convertFiles g-recaptcha btn shadow-none br_10 px-3 px-sm-4 py-1 pb-lg-2 mt-lg-1']"))
            )
            driver.execute_script("arguments[0].click();", convert_button)
            
            time.sleep(10)
            
            textarea = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "copyText_0"))
            )
            
            extracted_text = textarea.get_attribute('value')
            if "Error:- Uploaded Image does not contain any text" in extracted_text:
                raise Exception("Text extraction failed, error message received.")
            
            if extracted_text.strip() == '':
                raise Exception("Text extraction failed, textarea is empty.")
            
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{os.path.basename(image_path)}:\n{extracted_text}\n")
            
            print(f"Text extracted and written to file: {image_path}")
            return
            
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt}/{max_retries} - Error occurred: {e}")
            traceback.print_exc()
            driver.refresh()
            time.sleep(5)

    print(f"Text extraction failed after {max_retries} attempts: {image_path}")

def main_function(image_dir, output_file, output_dir):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith('.jpg')]
    
    processed_images = set()
    
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            continue
        
        if image_path in processed_images:
            print(f"Image already processed: {image_path}")
            continue
        
        left_path, right_path = split_image(image_path, output_dir)
        
        extract_and_write_text(left_path, output_file, driver)
        extract_and_write_text(right_path, output_file, driver)
        
        processed_images.add(image_path)
        
        time.sleep(2)
        
        driver.refresh()
        time.sleep(2)

    driver.quit()

image_dir = r'C:\Users\ytetl\OneDrive\Masaüstü\Image'
output_file = 'extracted_texts.txt'
output_dir = r'C:\Users\ytetl\OneDrive\Masaüstü\Image_Cut'

os.makedirs(output_dir, exist_ok=True)

main_function(image_dir, output_file, output_dir)
