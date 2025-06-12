from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'ini_rahasia_kelompok2'  # digunakan untuk flash message

# Ganti ini dengan URL endpoint Lambda API kamu
API_BASE = 'https://rvcybuvcg7.execute-api.us-east-1.amazonaws.com/dev/users'

@app.route('/')
def index():
    response = requests.get(API_BASE)
    if response.status_code == 200:
        users = response.json()
    else:
        users = []
        flash('Gagal mengambil data pengunjung')
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        pesan = request.form['pesan']
        payload = {'name': name, 'pesan': pesan}
        response = requests.post(API_BASE, json=payload)
        if response.status_code == 201:
            flash('Pengunjung berhasil ditambahkan!')
        else:
            flash('Gagal menambahkan pengunjung.')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    get_url = f"{API_BASE}"
    response = requests.get(get_url)
    users = response.json()
    user = next((u for u in users if u['id'] == id), None)

    if not user:
        flash('Pengunjung tidak ditemukan')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        payload = {'name': name}
        put_url = f"{API_BASE}/{id}"
        put_response = requests.put(put_url, json=payload)
        if put_response.status_code == 200:
            flash('Pengunjung berhasil diubah!')
        else:
            flash('Gagal mengubah data pengunjung.')
        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    delete_url = f"{API_BASE}/{id}"
    response = requests.delete(delete_url)
    if response.status_code == 204:
        flash('Pengunjung berhasil dihapus!')
    else:
        flash('Gagal menghapus pengunjung.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
