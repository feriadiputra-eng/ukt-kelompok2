from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_BASE_URL = 'https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/users'

@app.route('/')
def index():
    response = requests.get(API_BASE_URL)
    users = response.json()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'institution': request.form['institution'],
            'position': request.form['position'],
            'phone': request.form['phone']
        }
        requests.post(API_BASE_URL, json=data)
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
        }
        requests.put(f"{API_BASE_URL}/{id}", json=data)
        return redirect(url_for('index'))
    user = requests.get(f"{API_BASE_URL}/{id}").json()
    return render_template('edit_user.html', user=user)

@app.route('/delete/<id>', methods=['POST'])
def delete_user(id):
    requests.delete(f"{API_BASE_URL}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000, debug=True)
