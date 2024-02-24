from flask import Flask, session, redirect, url_for, request, render_template, jsonify
import requests
from BotFiles import bot, telegramBot
from BotFiles.generalFunctions import *

import threading

app = Flask(__name__)
app.secret_key = '29832'

Flask.debug = True
selected_mode = "light"


def get_users_data():
    try:
        res = requests.get('https://65d7cd1627d9a3bc1d7bcfc3.mockapi.io/api/usersData')
        return res.json()
    except Exception as e:
        print(e)
        return None


def confirm_account(email, company, telegram_api, telegram_password):
    all_registered_user = get_users_data()
    all_emails = [user['email'].lower().strip() for user in all_registered_user]
    if email.lower().strip() in all_emails:
        user_data = read_json_file('./static/assets/userData.json')
        user_data['email'] = email
        user_data['company-name'] = company
        user_data['telegram-api'] = telegram_api
        user_data['telegram-password'] = telegram_password
        write_json_file('./static/assets/userData.json', user_data)
        return True
    return False


user_data = read_json_file('./static/assets/userData.json')
user_data['bot-status'] = "Stopped"
write_json_file('./static/assets/userData.json', user_data)


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user_data = read_json_file('./static/assets/userData.json')
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    if user_data['email'] == "":
        return redirect(url_for('profile'))

    data = {
        "active": "dashboard",
        "selectedMode": selected_mode,
        "user": user_data,
        "attachAccount": attach_account
    }

    return render_template('index.html', data=data)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    user_data = read_json_file('./static/assets/userData.json')
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    data = {
        "active": "dashboard",
        "selectedMode": selected_mode,
        "user": user_data,
        "attachAccount": attach_account
    }

    if request.method == 'POST':
        email = request.form['email']
        company = request.form['company']
        telegram_api = request.form['telegram-api']
        telegram_password = request.form['telegram-password']
        if confirm_account(email, company, telegram_api, telegram_password):
            return redirect(url_for('dashboard'))
        else:
            # show error
            return redirect(url_for('profile'))

    return render_template('index.html', data=data)


@app.route('/history')
def history():
    user_data = read_json_file('./static/assets/userData.json')
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    if user_data['email'] == "":
        return redirect(url_for('profile'))

    data = {
        "active": "dashboard",
        "selectedMode": selected_mode,
        "user": user_data,
        "attachAccount": attach_account
    }
    return render_template('index.html', data=data)


@app.route('/drivers')
def drivers():
    user_data = read_json_file('./static/assets/userData.json')
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    if user_data['email'] == "":
        return redirect(url_for('profile'))

    data = {
        "active": "dashboard",
        "selectedMode": selected_mode,
        "user": user_data,
        "attachAccount": attach_account
    }
    return render_template('index.html', data=data)


@app.route('/settings')
def settings():
    user_data = read_json_file('./static/assets/userData.json')
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    print(attach_account, "attach_account")
    if user_data['email'] == "":
        return redirect(url_for('profile'))

    data = {
        "active": "dashboard",
        "selectedMode": selected_mode,
        "user": user_data,
        "attachAccount": attach_account
    }
    return render_template('index.html', data=data)


# backendRoutes
@app.route('/switch-mode', methods=['POST', 'GET'])
def switch_mode():
    global selected_mode
    if request.method == 'POST':
        selected_mode = "dark" if selected_mode == "light" else "light"
        print("Mode: ", selected_mode)
        return jsonify({"status": "success", "mode": selected_mode})

    return jsonify({"status": "success", "mode": selected_mode})


@app.route('/start-bot')
def start_bot():
    user_data = read_json_file('./static/assets/userData.json')
    if user_data['bot-status'] == "Running":
        user_data['bot-status'] = "Stopped"
    else:
        user_data['bot-status'] = "Running"
        threading.Thread(target=telegramBot.telegram_bot).start()
        threading.Thread(target=bot.start_bot).start()

    write_json_file('./static/assets/userData.json', user_data)
    return 'Bot Status: ' + user_data['bot-status']


@app.route('/attach-account')
def add_account():
    threading.Thread(target=bot.check_uber_account_attached).start()
    return 'Account is being attached'


@app.route('/remove-account')
def remove_account():
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    attach_account['attached'] = False
    write_json_file('./BotFiles/attachAccount.json', attach_account)
    return 'Account is being removed'


@app.route('/delete-history')
def delete_history():
    user_data = read_json_file('./static/assets/userData.json')
    user_data['history'] = []
    write_json_file('./static/assets/userData.json', user_data)
    return redirect(url_for('history'))





app.run(debug=False, host='0.0.0.0', port=5000)
