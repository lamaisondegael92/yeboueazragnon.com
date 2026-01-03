from flask import Flask, render_template, redirect, request, make_response

app = Flask(__name__)
app.config["SECRET_KEY"] = "change_plus_tard_en_production"

# -------------------------
# FONCTION DE VÉRIFICATION
# -------------------------
def verifier_acces():
    return request.cookies.get("abonneYT") == "true"

from flask import send_from_directory
import os

@app.route("/telecharger/bot-vbs-ranger-pc")
def telecharger_bot_vbs():
    if not verifier_acces():
        return redirect("/")

    chemin = os.path.join(app.root_path, "downloads", "gratuits")
    return send_from_directory(
        chemin,
        "bot_vbs_ranger_pc.zip",
        as_attachment=True
    )


# -------------------------
# PAGE DE VÉRIFICATION
# -------------------------
@app.route("/")
def verification():
    return render_template("verification.html")


# -------------------------
# VALIDATION ABONNÉ
# -------------------------
@app.route("/valider_abonne", methods=["POST"])
def valider_abonne():
    response = make_response(redirect("/index"))
    response.set_cookie(
        "abonneYT",
        "true",
        max_age=60 * 60 * 24 * 30,  # 30 jours
        httponly=True,
        samesite="Lax"
    )
    return response


# -------------------------
# PAGES PROTÉGÉES
# -------------------------
@app.route("/index")
def index():
    if not verifier_acces():
        return redirect("/")
    return render_template("index.html")


@app.route("/produits")
def produits():
    if not verifier_acces():
        return redirect("/")
    return render_template("produits.html")


@app.route("/formations")
def formations():
    if not verifier_acces():
        return redirect("/")
    return render_template("formations.html")


@app.route("/blog")
def blog():
    if not verifier_acces():
        return redirect("/")
    return render_template("blog.html")


@app.route("/contact")
def contact():
    if not verifier_acces():
        return redirect("/")
    return render_template("contact.html")


# -------------------------
# LANCEMENT LOCAL UNIQUEMENT
# (Render utilisera Gunicorn)
# -------------------------
if __name__ == "__main__":
    app.run()
