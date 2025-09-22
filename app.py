from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        gender TEXT,
                        contact TEXT,
                        address TEXT,
                        medical_concerns TEXT
                    )''')
    conn.commit()
    conn.close()


# --- Home (Read) ---
@app.route('/')
def index():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)


# --- Create (Add Patient) ---
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        concern = request.form['concern']

        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, contact, address, medical_concerns) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, age, gender, contact, address, concern))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


# --- Update (Edit Patient) ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        concern = request.form['concern']

        cursor.execute("""UPDATE patients 
                          SET name=?, age=?, gender=?, contact=?, address=?, medical_concerns=?
                          WHERE id=?""",
                       (name, age, gender, contact, address, concern, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()
    conn.close()
    return render_template('edit.html', patient=patient)


# --- Delete Patient ---
@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run()
