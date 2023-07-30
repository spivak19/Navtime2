import sqlite3
from flask import Flask, render_template, request


app = Flask(__name__, template_folder="templates", static_folder="staticFiles")

# Replace 'db_path' with the path to your SQLite database
db_path = "DataBase.db"

def get_table_data():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Replace 'your_table_name' with the name of the table you want to display
    cursor.execute('SELECT * FROM documents')
    rows = cursor.fetchall()
    conn.close()
    return rows

def author(X, DbPath):
    conn = sqlite3.connect(DbPath)
    c = conn.cursor()
    c.execute("SELECT * FROM documents WHERE (author=:px)", {"px": X})
    rows = c.fetchall()
    conn.close()
    return rows

def Title(X, DbPath):
    conn = sqlite3.connect(DbPath)
    c = conn.cursor()
    c.execute("SELECT * FROM documents WHERE instr(filename, ?) > 0;",[X])
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def display_table():
    table_data = get_table_data()
    return render_template('table.html', data=table_data)

@app.route("/action", methods = ['POST'])
def action():
    red = request.form.get('red')

    return render_template('table.html', red=red, data = Title("Sph",db_path))


if __name__ == '__main__':
    app.run(debug=True)