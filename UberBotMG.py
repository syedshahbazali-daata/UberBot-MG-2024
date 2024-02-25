from datetime import datetime

from flask import Flask, session, redirect, url_for, request, render_template, jsonify
import requests
from BotFiles import bot, telegramBot
from BotFiles.generalFunctions import *
import shutil
import os
import webview
import threading

app = Flask(__name__)
app.secret_key = '29832'

Flask.debug = True
selected_mode = "light"
ADMIN = False


def get_users_data():
    try:
        res = requests.get('https://65d7cd1627d9a3bc1d7bcfc3.mockapi.io/api/usersData')
        return res.json()
    except Exception as e:
        print(e)
        return None


def add_user_data(email, company):
    try:
        data = {
            "email": email.lower(),
            "company": company.title(),
            "current_date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "joining_date": ""
        }
        res = requests.post('https://65d7cd1627d9a3bc1d7bcfc3.mockapi.io/api/usersData', data=data)
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
    if ADMIN:
        return redirect(url_for('admin_manage_users'))
    user_data = read_json_file('./static/assets/userData.json')
    all_registered_user = get_users_data()
    all_emails = [user['email'].lower().strip() for user in all_registered_user]
    if user_data['email'] != "" and user_data['email'].lower().strip() in all_emails:
        return redirect(url_for('dashboard'))
    elif user_data['email'].lower().strip() not in all_emails:
        user_data['email'] = ""
        user_data['company-name'] = ""
        user_data['telegram-api'] = ""
        user_data['telegram-password'] = ""
        # messages-sent,drivers,history
        user_data['messages-sent'] = 0
        user_data['drivers'] = []
        user_data['history'] = []
        # attachAccount
        attach_account = read_json_file('./BotFiles/attachAccount.json')
        attach_account['attached'] = False
        write_json_file('./BotFiles/attachAccount.json', attach_account)
        write_json_file('./static/assets/userData.json', user_data)

        # delete userDir
        shutil.rmtree(os.path.join(os.getcwd(), "BotFiles", "userDir"), ignore_errors=True)
        # create new userDir
        os.mkdir(os.path.join(os.getcwd(), "BotFiles", "userDir"))

    return redirect(url_for('profile'))


@app.route('/dashboard')
def dashboard():
    attach_account = read_json_file('./BotFiles/attachAccount.json')
    user_data = read_json_file('./static/assets/userData.json')
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


# ADMIN PANEL


@app.route('/admin-manage-users')
def admin_manage_users():
    all_registered_user = get_users_data()
    data = {
        "allRegisteredUser": all_registered_user
    }

    return render_template('admin.html', data=data)


@app.route('/admin-add-user', methods=['POST', 'GET'])
def admin_add_user():
    all_registered_user = get_users_data()
    all_registered_user_emails = [user['email'].lower().strip() for user in all_registered_user]
    data = {
        "allRegisteredUser": all_registered_user,
        "allRegisteredUserEmails": all_registered_user_emails
    }

    if request.method == 'POST':
        email = request.form['email']
        company = request.form['company']
        if email.lower().strip() not in all_registered_user_emails and email != "":
            add_user_data(email, company)
            return redirect(url_for('admin_manage_users'))
        else:
            # show error
            return redirect(url_for('admin_add_user'))

    return render_template('admin.html', data=data)


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


@app.route('/delete-user/<user_id>')
def delete_user(user_id):
    try:
        requests.delete(f'https://65d7cd1627d9a3bc1d7bcfc3.mockapi.io/api/usersData/{user_id}')
        return redirect(url_for('admin_manage_users'))
    except Exception as e:
        print(e)
        return None


# app.run(debug=True, port=5000)
webview.create_window('UberBotMG', app, width=1200, height=800, maximized=True)
webview.start()
