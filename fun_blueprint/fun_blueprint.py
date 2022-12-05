from flask import Blueprint, render_template, request
from data_science.sentiment.sentiment_analysis import sentiment_analysis

fun_blueprint = Blueprint('fun_blueprint', __name__, template_folder="templates")

@fun_blueprint.route("/sentiment", methods=["GET", "POST"])
def sentiment_text():
    if request.method == "GET":
        # return("<h1>HELLO</h1>")
        return render_template("sentiment_template.html", params={"msg": None})
    else:
        msg = request.form.get("text")
        analysis = sentiment_analysis(msg)
        return render_template("sentiment_template.html", params={"msg": msg, "analysis": analysis})
