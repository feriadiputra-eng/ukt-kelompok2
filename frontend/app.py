from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'ini_rahasia_kelompok2'  # digunakan untuk flash message

# Ganti ini dengan URL endpoint Lambda API kamu
API_BASE = 'https://tn6ac8w6m8.execute-api.us-east-1.amazonaws.com/dev/users'

@app.route('/')
def index():
    try:
        response = requests.get(API_BASE)
        if response.status_code == 200:
            users = response.json()
        else:
            users = []
            flash('Gagal mengambil data pengunjung')
    except Exception as e:
        users = []
        flash(f'Terjadi kesalahan saat mengambil data: {str(e)}')
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        pesan = request.form.get('pesan')
        payload = {'name': name, 'pesan': pesan}
        try:
            response = requests.post(API_BASE, json=payload)
            if response.status_code == 201:
                flash('Pengunjung berhasil ditambahkan!')
            else:
                flash('Gagal menambahkan pengunjung.')
        except Exception as e:
            flash(f'Kesalahan saat menambahkan pengunjung: {str(e)}')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    try:
        response = requests.get(API_BASE)
        if response.status_code != 200:
            flash('Gagal mengambil data dari server')
            return redirect(url_for('index'))

        users = response.json()
        user = next((u for u in users if u['id'] == id), None)
        if not user:
            flash('Pengunjung tidak ditemukan')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name')
            pesan = request.form.get('pesan')
            payload = {'name': name, 'pesan': pesan}
            put_url = f"{API_BASE}/{id}"
            put_response = requests.put(put_url, json=payload)
            if put_response.status_code == 200:
                flash('Pengunjung berhasil diubah!')
            else:
                flash('Gagal mengubah data pengunjung.')
            return redirect(url_for('index'))

        return render_template('edit_user.html', user=user)

    except Exception as e:
        flash(f'Kesalahan saat mengedit data: {str(e)}')
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        delete_url = f"{API_BASE}/{id}"
        response = requests.delete(delete_url)
        if response.status_code == 204:
            flash('Pengunjung berhasil dihapus!')
        else:
            flash('Gagal menghapus pengunjung.')
    except Exception as e:
        flash(f'Kesalahan saat menghapus pengunjung: {str(e)}')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
