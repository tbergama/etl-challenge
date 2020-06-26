from flask import Flask, jsonify, render_template, redirect


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
    article = db.mars_data.find_one({"item": "news_article"})
    jpl_image = db.mars_data.find_one({"item": "jpl_image"})
    weather = db.mars_data.find_one({"item": "weather"})
    facts = db.mars_data.find_one({"item": "facts"})
    hemispheres = db.mars_data.find_one({"item": "hemispheres"})

    return render_template(
        "index.html",
        article_title = article['title'],
        article_paragraph = article['paragraph'],
        jpl_image_url = jpl_image['image_url'],
        current_weather = weather['weather'],
        facts_html = facts['facts'],
        hemi_1 = hemispheres['hemispheres'][0]['img_url'],
        hemi_2 = hemispheres['hemispheres'][1]['img_url'],
        hemi_3 = hemispheres['hemispheres'][2]['img_url'],
        hemi_4 = hemispheres['hemispheres'][3]['img_url']
    )

@app.route("/scrape")
def scrape_route():

    # Scrape mars data
    data = scrape_mars.scrape()

    # Delete old document
    db.mars_data.delete_many({})

    # Insert newly scraped data
    db.mars_data.insert_many(data)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
