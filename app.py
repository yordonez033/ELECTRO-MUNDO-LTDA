from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear la tabla si no existe
def crear_base():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS personas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL
                    )""")
    conn.commit()
    conn.close()

crear_base()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]

        # Guardar en la base de datos
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personas (nombre) VALUES (?)", (nombre,))
        conn.commit()
        conn.close()
        return redirect("/lista")
    
    return render_template("formulario.html")

@app.route("/lista")
def lista():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    conn.close()
    return render_template("lista.html", personas=personas)

if __name__ == "__main__":
    app.run(debug=True)