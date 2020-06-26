from flask import Flask, jsonify

import pymongo

import scrape_mars

# Set up PyMongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# Set up flask
app = Flask(__name__)

@app.route("/")
def homepage():
    """List available routes on homepage"""
    return (
        "Mars scrape"
    )

@app.route("/scrape")
def scrape_route():

    # Scrape mars data
    data = scrape_mars.scrape()

    # Delete old document
    db.mars_data.delete_many({})

    # Insert newly scraped data
    db.mars_data.insert_many(data)

    return("scrape complete")

if __name__ == '__main__':
    app.run(debug=True)
