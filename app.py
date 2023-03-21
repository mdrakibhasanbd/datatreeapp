from flask import Flask, render_template
from flask_cors import CORS
import pymongo
import json

app = Flask(__name__)
cors = CORS(app)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['device']
collection = db['data']


@app.route("/")
def home():
    return render_template('index.html')



@app.route("/tree")
def tree():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["device"]
    collections = mydb.data.find()



    data = []

    for i in collections:
        data.append(i)
        # print(data)

    id_mapping = {}
    for i, el in enumerate(data):
        id_mapping[el['_id']] = i

    root = None
    for el in data:
        # Handle the root element
        # if el['parentId'] is "null":
        if el['parentId'] == None:
            root = el
            continue
        # Use our mapping to locate the parent element in our data array
        parent_el = data[id_mapping[el['parentId']]]
        # Add our current el to its parent's `children` list
        parent_el['children'] = parent_el.get('children', []) + [el]

    jsn = json.dumps(root, indent=4)
    print(jsn)

    return jsn

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
