from flask import Flask, render_template
from admin import admin_bp  

app = Flask(__name__, template_folder="templates")

app.register_blueprint(admin_bp)

# ROTA PRINCIPAL (CLIENTE)
@app.route("/")
def index():
    return render_template("index.html", pagina="home")

if __name__ == "__main__":
    app.run(debug=True)
