from selenium import webdriver
import os
import requests
from selenium.webdriver.common.by import By
from .generalFunctions import *
import time

# current path

USER_DIR = os.path.join(os.getcwd(), "BotFiles", "UserDir")
# USER_DIR = r"C:\Users\hp\PycharmProjects\MG BOT - Al karwani\test\USER_DIR"
BASE_DIR = os.path.join(os.getcwd(), "BotFiles")
BOT_RUNNING = False
print(USER_DIR)

# token for the bot
token = read_json_file(os.path.join(os.getcwd(), "static", "assets", "userData.json"))['telegram-api']


def send_message(chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url)
    print(f"Message sent to {chat_id} with status code {res.status_code}")
    return None


def find_chat_id_by_surname(surname):
    user_data = read_json_file(os.path.join(os.getcwd(), "static", "assets", "userData.json"))
    drivers = user_data['drivers']
    for driver in drivers:
        if driver['surname'] == surname:
            return driver['chat_id']
    return None


def check_uber_account_attached():
    global BOT_RUNNING

    if BOT_RUNNING:
        return

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={USER_DIR}")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://vsdispatch.uber.com/")

    while True:
        attach_account = read_json_file(os.path.join(BASE_DIR, "attachAccount.json"))
        print(attach_account)
        if attach_account['attached']:
            time.sleep(5)
            break
        else:
            time.sleep(1)

    # Close the driver

    driver.quit()
    BOT_RUNNING = False


def start_bot():
    # GENERAL FUNCTIONS FOR BOT

    checks = 0

    global BOT_RUNNING

    attach_account = read_json_file(os.path.join(BASE_DIR, "attachAccount.json"))

    if BOT_RUNNING:
        return

    if not attach_account['attached']:
        return "Account is not attached"

    BOT_RUNNING = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={USER_DIR}")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://vsdispatch.uber.com/")

    while True:

        # checking if the bot is stopped
        user_data = read_json_file(os.path.join(os.getcwd(), "static", "assets", "userData.json"))
        bot_status = user_data['bot-status']
        if bot_status == "Stopped":
            driver.quit()
            BOT_RUNNING = False
            break
        else:
            time.sleep(1)

        # waiting for the ACCEPT ALL button to be enabled else keep waiting
        try:
            driver.find_element(By.XPATH, '//button[@data-testid="acceptall-btn" and not(@disabled)]')

            # prices,pickup,dropoff,rider,suggested_driver,date,time
            price_column = driver.find_elements(By.XPATH, '//table/tbody//td[2]')
            pickup_column = driver.find_elements(By.XPATH, '//table/tbody//td[3]')
            dropoff_column = driver.find_elements(By.XPATH, '//table/tbody//td[4]')
            rider_column = driver.find_elements(By.XPATH, '//table/tbody//td[5]')
            suggested_driver_column = driver.find_elements(By.XPATH, '//table/tbody//td[6]')
            date_column = driver.find_elements(By.XPATH, '//table/tbody//td[7]')
            time_column = driver.find_elements(By.XPATH, '//table/tbody//td[8]')

            # Clicking the ACCEPT ALL button
            while True:
                try:
                    element = driver.find_element(By.XPATH, '//button[@data-testid="acceptall-btn" and not(@disabled)]')
                    webdriver.ActionChains(driver).move_to_element_with_offset(element, 1, 0).click(element).perform()
                    break
                except Exception as e:
                    # print(e)
                    pass

            print("Button clicked")
            # Getting the data
            prices = [x.text for x in price_column]
            pickups = [x.text for x in pickup_column]
            dropoffs = [x.text for x in dropoff_column]
            riders = [x.text for x in rider_column]
            suggested_drivers = [x.text for x in suggested_driver_column]
            dates = [x.text for x in date_column]
            times = [x.text for x in time_column]

            # Creating the data in a dictionary (price,pickup,dropoff,rider,suggested_driver,date,time)
            data = [
                {
                    "price": prices[i],
                    "pickup": pickups[i],
                    "dropoff": dropoffs[i],
                    "rider": riders[i],
                    "suggested_driver": suggested_drivers[i],
                    "date": dates[i],
                    "time": times[i]
                }
                for i in range(len(prices))
            ]

            # send the data to the telegram bot
            no_of_messages = user_data['messages-sent']
            for single_alert in data:
                alert_message = f"{single_alert['price']} | {single_alert['rider']}\nPickup: {single_alert['pickup']}\n-->\nDropoff: {single_alert['dropoff']}"
                chat_id = find_chat_id_by_surname(single_alert['suggested_driver'])
                if chat_id is not None:
                    send_message(chat_id, alert_message)
                    print(f"Message sent to {single_alert['suggested_driver']}")
                    no_of_messages += 1
                else:
                    print(f"Chat ID not found for {single_alert['suggested_driver']}")

            print(data, "Data appended to the user data file")

            # append the data in user_data['history']
            user_data['history'].extend(data)
            user_data['messages-sent'] = no_of_messages
            write_json_file(os.path.join(os.getcwd(), "static", "assets", "userData.json"), user_data)
            print("Data appended")

            while True:
                try:
                    driver.find_element(By.XPATH, '//button[@data-testid="acceptall-btn" and @disabled]')
                    print("Button is disabled")
                    break
                except:
                    pass



        except:
            checks += 1
            if checks > 50:
                driver.refresh()
                print("Refreshing the page")
                checks = 0
            continue
