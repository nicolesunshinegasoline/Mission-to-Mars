from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
from config import password

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
# connect to Mongo using a URI, a uniform resource identifier similar to a URL
    # reach Mongo through our localhost server using port 27017
    # Using a database named "mars_app"
    
# client = pymongo.MongoClient(f"mongodb+srv://nicoleardizzi:{password}@cluster0.3ykjg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.test
app.config["MONGO_URI"] = f"mongodb+srv://nicoleardizzi:{password}@cluster0.3ykjg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)

# define the route for the HTML page
# tell Flask what to display when we're looking at the home page
@app.route("/")
def index():
   # use PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # tell Flask to return an HTML template using an index.html file
        # mars=mars tells Python to use the "mars" collection in MongoDB
   return render_template("index.html", mars=mars)

# add the scraping route
# this route will be the "button" of the web application, 
# the one that will scrape updated data when we tell it to from the homepage of our web app
@app.route("/scrape")
def scrape():
   # assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # create a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   # After gathering new data, update the database using .update_one()
       #
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   print(mars)
   return redirect('/', code=302)

# Tell flask to run
if __name__ == "__main__":
   app.run()
