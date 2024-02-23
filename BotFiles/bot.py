from selenium import webdriver
import os
import json
import time

# current path

USER_DIR = os.path.join(os.getcwd(), "BotFiles", "UserDir")
BASE_DIR = os.path.join(os.getcwd(), "BotFiles")
BOT_RUNNING = False
print(USER_DIR)


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except:
        print("Error in reading file")
        return None


def write_json_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except:
        print("Error in writing file")
        pass


def check_uber_account_attached():

    if BOT_RUNNING:
        return

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={USER_DIR}")
    chrome_options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://vsdispatch.uber.com/")

    while True:
        attach_account = read_json_file(os.path.join(BASE_DIR, "attachAccount.json"))
        print(attach_account)
        if attach_account['attached']:
            time.sleep(5)
            break
        else:
            time.sleep(1)


    # Close the browser
    browser.quit()
