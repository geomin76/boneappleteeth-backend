import requests
import json
from flask import Flask, request
from dotenv import load_dotenv
import os
import random

app = Flask(__name__)

load_dotenv()

@app.route("/")
def main():
    return "hello, world!"

@app.route("/restaurants")
def restaurants():
    url = "https://api.yelp.com/v3/graphql"
    headers = {
        "Authorization": "Bearer {}".format(os.environ.get('API_KEY')),
        "Content-Type": "application/graphql"    
    }
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    price = ""
    if request.args.get('price'):
        price += ", price: \"{}\"".format(request.args.get('price'))
    print(price)

    countQuery = """
    {
        search(term: "restaurants", latitude: """ + lat + """, longitude: """ + lng + """, open_now: true""" + price + """) {
            total
        }
    }
    """
    r = requests.post(url, headers=headers, data=countQuery)
    count_restaurants = int(json.loads(r.text)['data']['search']['total'])
    print("Number of restaurants {}".format(count_restaurants))

    random_digit = round(random.uniform(0, 0.5), 2)
    offset = int(count_restaurants * random_digit)
    print("Offset {}".format(offset))

    # create some algorithm that gets total number of restaurants then creates offset randomizer (certain percentage)
    # so if user at frontend goes through all restaurants, query a new number of restaurants, need to do a "hit" list for random in frontend

    query = """
    {
        search(term: "restaurants", latitude: """ + lat + """, longitude: """ + lng + """, open_now: true, offset: """ + str(offset) + price + """) {
            total
            business {
                name
            }
        }
    }
    """
    
    r = requests.post(url, headers=headers, data=query)
    print(r.status_code)
    json_data = json.loads(r.text)
    return json_data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)