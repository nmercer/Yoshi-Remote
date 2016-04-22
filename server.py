from flask import request, jsonify, Flask
import json
import re
import requests

app = Flask(__name__)

@app.route('/yoshi/')
def home():
    return "Yoshi Smarthome Endpoint"

# For parsing chase alerts. IFTTT and sms to get a sms every time I spend moeny.
@app.route('/yoshi/chase/', methods=['POST'])
def chase():
    email = str(request.get_data()).strip('\t\n\r')
    if "This is an Alert" in email:
    	charge = re.findall("\d+\.\d+", re.findall('A charge of[\s\S]*at', email)[0].replace('A charge of', '').replace('at', '').strip())[0]
    	place = re.findall('at[\s\S]*has been', email)[0].replace('at', '').replace('has been', '').strip()
    	sms = "$%s at %s" % (charge, place)
    	maker_url = "https://maker.ifttt.com/trigger/chase/with/key/cfBaalraUFXTVNPOtnTP_3"
    	requests.post(maker_url, data = {'value1':sms})
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8002)
