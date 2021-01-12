from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request,
    url_for,
    flash,
    Response,
    make_response,
    Markup,
)

from flask_bcrypt import Bcrypt

app = Flask(__name__) 

@app.route("/")
def index():
    return render_template("Hello world") 

if __name__ == "__main__":
    app.run(debug=True)