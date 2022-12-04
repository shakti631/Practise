from flask import Blueprint, render_template, request

fun_blueprint = Blueprint('fun_blueprint', __name__, template_folder="templates")

@fun_blueprint.route("/sentiment", methods=["GET", "POST"])
def sentiment_text():
    if request.method == "GET":
        # return("<h1>HELLO</h1>")
        return render_template("sentiment_template.html")
    else:
        msg = request.form.get("text")
        return f"<h1>{msg}</h1>"