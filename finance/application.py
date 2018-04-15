from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, calculate_shares

# Configure application
app = Flask(__name__)
app.jinja_env.globals.update(usd=usd)
# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Shows the current portfolio"""
    # Get transactions from database
    transactions = db.execute("SELECT Symbol, Name, shares, price FROM portfolio WHERE User_ID = :id",
                              id=session["user_id"])

    # Calculate the shares
    shares = calculate_shares(transactions)

    # Add the current price etc. to the shares.
    shares_cash = 0
    cash = 0
    for trans in range(len(shares)):
        symbol = shares[trans]["Symbol"]
        product = lookup(symbol)
        currentprice = float(product["price"])
        shares[trans]["currentprice"] = currentprice
        shares_price = float(shares[trans]["shares"] * currentprice)
        shares[trans]["shares_price"] = shares_price
        shares_cash += shares_price
        cash += shares[trans]["buying_costs"]

    cash = 10000 - cash

    # Prepare the table content
    for trans in range(len(shares) - 1):
        if shares[trans]["shares"] == 0:
            del shares[trans]

    return render_template("index.html", stocks=shares, cash=cash, total=cash
                           + shares_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        total = 0.0
        product = request.form.get("symbol")
        shares_quantity = request.form.get("shares")
        if not request.form.get("shares").isdigit():
            return apology("INVALED SYMBOL", 400)
        if not product:
            return apology("MISSING SYMBOL", 400)
        elif not shares_quantity:
            return apology("MISSING SHARES", 400)
        x = lookup(product)
        if not x:
            return apology("Not exist", 400)
        if int(shares_quantity) < 0:
            return apology("INVALED SYMBOL", 400)
        total = int(shares_quantity) * float(x["price"])
        row = db.execute("SELECT * FROM users WHERE id = :id",
                         id=session["user_id"])

        cash = row[0]["cash"]
        if total > cash:
            return apology("INVALED SHARES", 400)

        row = db.execute("UPDATE USERS SET cash = :cash WHERE ID = :User_ID",
                         User_ID=session["user_id"], cash=cash - total)
        row = db.execute("INSERT into portfolio(Symbol,Name,price,shares,User_ID) VALUES(:Symbol,:Name,:price,:shares,:User_ID)",
                         User_ID=session["user_id"], Symbol=x["symbol"], Name=x["name"], price=x["price"], shares=shares_quantity)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    histories = db.execute(
        "SELECT Symbol, shares, price,Excute_Date from portfolio WHERE User_ID = :id", id=session["user_id"])
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        product = lookup(request.form.get("symbol"))
        if not product:
            return apology("INVALID SYMBOL", 400)
        return render_template("validquote.html", name=product["name"], symbol=product["symbol"], price=usd(product["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("Must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("Must provide confirmation password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)
        hashes = generate_password_hash(request.form.get("password"))

        # Inserting the new user
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hashes)
        if not result:
            return apology("Username already exist", 400)

         # remember which user has logged in
        session["user_id"] = result
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        total = 0.0
        product = request.form.get("symbol")
        shares_quantity = int(request.form.get("shares"))
        if not product:
            return apology("MISSING SYMBOL", 400)
        elif not shares_quantity:
            return apology("MISSING SHARES", 400)
        x = lookup(product)
        total = int(shares_quantity) * float(x["price"])
        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

        cash = row[0]["cash"]
        current_shares_row = db.execute("SELECT sum(shares) as balance FROM portfolio WHERE User_ID = :id and symbol = :symbol",
                                        id=session["user_id"], symbol=product)
        current_shares = current_shares_row[0]["balance"]
        if current_shares < shares_quantity:
            return apology("wrong SHARES", 400)
        shares_quantity = shares_quantity * -1
        row = db.execute("UPDATE USERS SET cash = :cash WHERE ID = :User_ID",
                         User_ID=session["user_id"], cash=cash + total)
        row = db.execute("INSERT into portfolio(Symbol,Name,price,shares,User_ID)VALUES(:Symbol,:Name,:price,:shares,:User_ID)",
                         User_ID=session["user_id"], Symbol=x["symbol"], Name=x["name"], price=x["price"], shares=shares_quantity)

        return redirect("/")
    else:
        rows = db.execute("select distinct symbol as distintSymbol from portfolio where User_ID = :id",
                          id=session["user_id"])
        return render_template("sell.html", SymbolName=rows)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
