from http import client
from flask import Flask, redirect, request, render_template
import json
import pymongo
import requests
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/pincode')
@app.route('/pincode')
def pincode():
    return render_template('index.html')




@app.route('/create_file', methods=['POST'])
def create_file():
    if request.method == 'POST':  
    

    
        pinc=json.loads(request.data)
        
        newurl="https://api.postalpincode.in/pincode/"+pinc["pin"]
        x = requests.get(newurl)
        # print(x.status_code)
        if x.status_code == 200:
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db=client["SagarDaTaBase"]
            data=x.json()[0]
            # print(db)  #   printing database

            # filter = {"Pincode":pinc["pin"]}
            # update = {"$set":data}
            # result = db.post.update_one(filter, update, upsert=True)
            # print(result)
            
            # return x.json()[0]
            # print(data)
            try:

                dt =data["PostOffice"]
                pin=dt[0]
                # print(pin['Pincode'])
                data['_id'] = pin['Pincode']
                
                db.post.insert_one(data)
                # source=data
                # source.PostOffice['Origin']='API'
                print("Data Inserted into Database")
                # print(data)
                return data
        
            except DuplicateKeyError:

                # print(data)

                results =db.post.find_one({"_id": pinc["pin"]})

                print("data already stored")
                # print(results)
                results['Origin'] = 'MongoDB'
                # results.insert(PostOffice['Origin']:'MongoDB')
                return results









if __name__ == "__main__":
    app.run(debug=True)