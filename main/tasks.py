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

from django.conf import settings
from pathlib import Path
@shared_task
def run_appium_test(pk):
    print(f"Running Appium test for PK: {pk}")
    app=App.objects.get(pk=pk)
    print("========= file ",app.apk_file_path,app.screen_changed)
    full_path = Path(settings.BASE_DIR) / str(app.apk_file_path)
    # app.screen_changed=True
    app.save()
    def get_driver():
        desired_caps = {
        'platformName': 'Android',
        'platformVersion': '13.0',
        'deviceName': 'f5c6a6ba',
        'app': str(full_path),  # Path to your APK
        'automationName': 'UiAutomator2',
        'appPackage': 'com.example.todo',  # Adjust as needed
        'autoGrantPermissions': True
        }
        

    # Use AppiumOptions instead of webdriver.Remote directly
        options = AppiumOptions()
        for key, value in desired_caps.items():
          options.set_capability(key, value)

        return webdriver.Remote('http://appium:4723', options=options)

    def capture_screenshot(driver, filename):
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))
        image.save(filename)

    def record_video(driver, output_file):
        # Start video recording
        driver.start_recording_screen()

        # Perform actions
        time.sleep(10)  # Adjust time as needed

        # Stop recording and save video
        video_base64 = driver.stop_recording_screen()
        video_data = base64.b64decode(video_base64)
        with open(output_file, 'wb') as f:
            f.write(video_data)
    
    
    base=settings.BASE_DIR / settings.MEDIA_ROOT
    driver = get_driver()
    try:
        # Capture initial screen
        initial_screenshot_path = Path(base) / 'initial_screen.png'
        capture_screenshot(driver, initial_screenshot_path)
        
        # Get UI elements
        ui_elements = driver.page_source
        
        # Simulate click on the first button
        buttons = driver.find_elements(MobileBy.CLASS_NAME, 'android.widget.Button')
        if buttons:
            buttons[0].click()
            time.sleep(5)  # Wait for potential screen change

            # Capture subsequent screen
            subsequent_screenshot_path =Path(base) / 'subsequent_screen.png'
            capture_screenshot(driver, subsequent_screenshot_path)

            # Check if the screen has changed
            screen_changed = not os.path.samefile(initial_screenshot_path, subsequent_screenshot_path)
        else:
            screen_changed = False
            subsequent_screenshot_path = None

        # Record video
        video_path =Path(base) / 'video.mp4'
        
        print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ",video_path,base)
        record_video(driver, video_path)
        with open(video_path, 'rb') as f:
            app.video_recording_path.save('video.mp4', File(f))
        with open(initial_screenshot_path, 'rb') as f:
            app.first_screenshot_path.save('initial_screen.png', File(f))
        with open(subsequent_screenshot_path, 'rb') as f:
            app.second_screenshot_path.save('subsequent_screen.png', File(f))
            
            print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # app.first_screenshot_path.save(initial_screenshot_path)
        # app.screen_changed=screen_changed
        # app.second_screenshot_path.save(subsequent_screenshot_path)
        # app.video_recording_path.save(video_path)
        app.ui_hierarchy=json.dumps(ui_elements)
        # Save data to Django model
        # app = App(
        #     name='Sample App',
        #     initial_screen_screenshot=initial_screenshot_path,
        #     subsequent_screen_screenshot=subsequent_screenshot_path,
        #     video_recording=video_path,
        #     ui_elements=json.dumps(ui_elements),
        #     screen_changed=screen_changed
        # )
        # app.subsequent_screenshot_path=subsequent_screenshot_path
        # app.first_screenshot_path=initial_screen_screenshot
        app.save()
        

    finally:
        driver.quit()
        # os.remove('initial_screen.png')
        # os.remove('after_click_screen.png')
        # os.remove('test_video.mp4')
