# tasks.py
from celery import shared_task
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy as MobileBy
from appium.options.common.base import AppiumOptions
from django.conf import settings
from .models import App
import os
import time
import base64
from PIL import Image
import json
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from django.conf import settings
from pathlib import Path
from PIL import Image
import io
import hashlib
@shared_task
def run_appium_test(pk):
    print(f"Running Appium test for PK: {pk}")
    app=App.objects.get(pk=pk)
    full_path = Path(settings.BASE_DIR) / str(app.apk_file_path)
    

    def get_driver():
        desired_caps = {
        'platformName': 'Android',
        'platformVersion': '13.0',
        'deviceName': 'f5c6a6ba',
        'app': str(full_path), 
        'automationName': 'UiAutomator2',
        'appPackage': 'com.example.todo', 
        'autoGrantPermissions': True
        }
        

    # Use AppiumOptions instead of webdriver.Remote directly
        options = AppiumOptions()
        for key, value in desired_caps.items():
            options.set_capability(key, value)

        return webdriver.Remote('http://appium:4723', options=options)

    def capture_screenshot(driver):
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))
        image_buffer = BytesIO()
        image.save(image_buffer,format='PNG')
        image_bytes = image_buffer.getvalue()
        image_buffer.close()
        return image_bytes

    def start_record_video(driver):
        driver.start_recording_screen()

        
    
    def stop_record_video(driver):
        driver.start_recording_screen()
        time.sleep(10)
        # driver.stop_recording_screen()
        video_base64 = driver.stop_recording_screen()
        video_data = base64.b64decode(video_base64)
        return video_data

    def get_image_hash(image_bytes):
        """
        Generate a hash for the given image bytes.
        """
        image = Image.open(io.BytesIO(image_bytes))
        hasher = hashlib.md5()  # You can use sha256 or another algorithm as well
        hasher.update(image.tobytes())
        return hasher.hexdigest()

    def compare_images(image_bytes1, image_bytes2):
        """
        Compare two images in bytes to see if they are the same.
        """
        hash1 = get_image_hash(image_bytes1)
        hash2 = get_image_hash(image_bytes2)
        return hash1 == hash2

    driver = get_driver()
    try:
        # Capture initial screen
        # start_record_video(driver)
        driver.start_recording_screen()
        time.sleep(5)
        first_bytes =capture_screenshot(driver)
        app.first_screenshot_path.save('initial_screen.png', ContentFile(first_bytes))
        # Get UI elements
        ui_elements = driver.page_source
        
        # Simulate click on the first button
        buttons = driver.find_elements(MobileBy.CLASS_NAME, 'android.widget.Button')
        if buttons:
            buttons[0].click()
            time.sleep(5)  # Wait for potential screen change


            second_bytes=capture_screenshot(driver)
            app.second_screenshot_path.save('subsequent_screen.png', ContentFile(second_bytes))

            # Check if the screen has changed
            screen_changed = not compare_images(first_bytes, second_bytes)
        else:
            screen_changed = False

        # driver.start_recording_screen()
        time.sleep(10)
        # driver.stop_recording_screen()
        video_base64 = driver.stop_recording_screen()
        video_data = base64.b64decode(video_base64)
        # return video_data
        # video_data = stop_record_video(driver)
        video_data = base64.b64decode(video_base64)
        if len(video_data) > 0:
            app.video_recording_path.save('video.mp4', ContentFile(video_data))
            print("vid------------ ",len(video_data))
        else:
            app.video_recording_path = None
            print("vid------------ ",len(video_data))
            

        app.screen_changed=screen_changed

        app.ui_hierarchy=json.dumps(ui_elements)

        app.save()
        

    finally:
        driver.quit()

