import random
import string
from flask import Flask, render_template, redirect, request
from rate_limit import create_limiter
from database import Database





app = Flask(__name__)

limiter = create_limiter(app)

#instantiation of the database class
db = Database()


#Generates a short url when a long url is entered
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.route("/", methods =["GET","POST"])
@limiter.limit("8 per minute")
def index():

    if request.method == "POST":
        print("POST request received")  # For debugging
        
        long_url = request.form["long_url"]
        conn = db.connect()
        cursor = conn.cursor()

        while True:
            short_url = generate_short_url()
            cursor.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))
            if not cursor.fetchone():  # If short URL does not exist
                break

        cursor.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
        conn.commit()
        
        print(f"Inserted {short_url} -> {long_url} into database")  # For debugging

        cursor.close()
        conn.close()


        return render_template("success.html", short_url = f"{request.url_root}{short_url}")
        #return f"Shortened URL: {request.url_root}{short_url}"  # Return shortened URL

    # This part will be reached for GET requests (when the page is loaded)
    print("GET request received")  # For debugging
    return render_template("index.html")  # Render the form for GET request


@app.route("/<short_url>")
def redirect_url(short_url):
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT long_url FROm urls WHERE short_url = %s", (short_url,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row :
        return redirect(row[0])
    else:
        return "URL not found",404
    


 #This method is used to go to the limit exceed page once the rate limit is reached.   
@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("limit_exceeded.html"),429


#This is just to return to the home page when the limit rate is exceeded
@app.route("/home", methods =["GET"])
def home():
    return render_template("index.html")


if __name__== "__main__":
    app.run(debug=True)
    