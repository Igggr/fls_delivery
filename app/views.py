from app import app


@app.route("/")
def index():
    return 'index'


@app.route("/cart/")
def cart():
    return "card"


@app.route("/account/")
def account():
    return "account"


@app.route("/login/")
def login():
    return "login"


@app.route('/logout/')
def logout():
    return "logout"

