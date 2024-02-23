from flask import Flask, session, redirect, url_for, request, render_template, jsonify

app = Flask(__name__)
app.secret_key = '29832'

Flask.debug = True
selected_mode = "light"


@app.route('/')
def index():

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    print(session)
    data = {
        "active": "dashboard",
        "selectedMode": selected_mode
    }

    return render_template('index.html', data=data)


@app.route('/profile')
def profile():
    data = {
        "active": "profile",
        "selectedMode": selected_mode
    }
    return render_template('index.html', data=data)


@app.route('/history')
def history():
    data = {
        "active": "history",
        "selectedMode": selected_mode

    }
    return render_template('index.html', data=data)


@app.route('/drivers')
def drivers():
    data = {
        "active": "drivers",
        "selectedMode": selected_mode
    }
    return render_template('index.html', data=data)


@app.route('/settings')
def settings():
    data = {
        "active": "settings"
    }
    return render_template('index.html', data=data)


@app.route('/logout')
def logout():
    data = {
        "active": "logout"
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


app.run(debug=True, host='0.0.0.0', port=5000)
