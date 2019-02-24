from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_collection.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    mars_news = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_collection.update({}, mars_news, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)