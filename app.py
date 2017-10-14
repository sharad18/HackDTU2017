import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)

page_token = "EAAFE2AB12bUBAEdWAU672nnZCqZBmRT2ZAdk8WhWDy7X5YR9rFlVcYtX4uyQsLi9Kv6NyLRfQo3ZAlUkCD2Nl0dFKZBQKEIchUfRWbwoiEFTaPCJs2fMWMnOiEtlW8eN9fkgz8Y14OZAHpTqLN0UfZB2hPJjkIO5jZCWPNzOPh8XTgZDZD"
verify_token = '2318934571'
PAGE_ACCESS_TOKEN = page_token

@app.route('/webhook', methods = ['GET'])
def verify():
	if request.args.get("hub.mode") == "suscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == verify_token:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200

	return "Hello world", 200

def logg(mess, meta='log', symbol='#'):
	#pass
	print ('%s\n%s\n%s'%(symbol*20,mess,symbol*20))

@app.route('/webhook', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)
	if data['object'] =="page":
		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:
				if messaging_event.get("message"):
					sender_id = messaging_event["sender"]["id"]
					recipient_id = messaging_event["recipient"]["id"]
					message_text = messaging_event["message"]["text"]
					print (sender_id)
					send_message(sender_id, "roger that!")

				if messaging_event.get("delivery"):
					pass
				if messaging_event.get("optin"):
					pass
				if messaging_event.get("postback"):
					print ("postback detected")
					sender_id = messaging_event["sender"]["id"]
					handle_postback(sender_id, messaging_event['postback']['payload'])
	return "ok", 200

def send_message(recipient_id, message_text):
	log("sending message to {recipient}: {text}".format(recipient = recipient_id, text = message_text))

	params = {
		"access_token": page_token
	}
	headers = {
		"Content-Type": "application/json"
	}
	data = json.dumps({
		"recipient": {
			"id": recipient_id
		},
		"message": {
			"text": message_text
		}
		})
	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
	if r.status_code != 200:
		log(r.status_code)
		log(r.text)

def set_persistant_menu():
	post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?acess_token=%s"%PAGE_ACCESS_TOKEN

	menu_object = {
		"setting_type": "call_to_actions",
		"thread_state": "existing_thread",
		"call_to_actions":[
			{
				"type":"postback",
				"title":"Cancer Prediction",
				"payload":"MENT"
			},
			{
				"type":"postback",
				"title":"Doctor Consultation",
				"payload":"DOCC"
			},
			{
				"type":"postback",
				"title":"Donate",
				"payload":"DONA"
			}

		]
}
menu_object = json.dumps(menu_object)
status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=menu_object)
logg(status.json(), symbol='----**----')
pprint(status.json())

def handle_postback(fbid, payload):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?acess_token=%s'%PAGE_ACCESS_TOKEN
	logg(payload, symbol='*')
	response_text = ''
	response_object = ''

	if payload == 'MENT':
		response_object = {
			"recipient":{
				"id":fbid
			},
			"message":{
				"attachment":{
					"type":"template",
					"payload":{
						"template_type":"generic",
						"elements":[
						{
							"title": 'Breast Cancer',
							"image_url":'https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.IMayXaX_hBCy4xVyLR6wzgEsDB%26pid%3D15.1&f=1',
							"subtitle": "Breast Cancer Prediction",
							"buttons":[
								{
									"type":"web_url",
									"url":'',
									"title":"Breast Cancer Prediction"
								}
							]
						},
						{
							"title": "Lung Cancer",
							"image_url": 'https://images.duckduckgo.co"m/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.TrjWtZh-FKEMhrPWM4MZCQEgDY%26pid%3D15.1&f=1',
							"subtitle" : "Lung Cancer Prediction",
							"buttons" :[
								{
									"type":"web_url",
									"url": '',
									"title":"Lung Cancer Prediction"
								}
							]
						},
						{
							"title": "Kidney Cancer",
							"image_url":'https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.TiU4Mc9aWCAD7n53SPtZ1gEsDI%26pid%3D15.1&f=1',
							"subtitle": "Lung Cancer Prediction",
							"buttons":[
								{
									"type":"web_url",
									"url":'',
									"title":"Kidney Cancer Prediction"
							}
						]
					},
					{
						"title": "Liver Cancer",
						"image_url":'https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.p5YwzFPviZavBSwXMvkLSAEsEO%26pid%3D15.1&f=1',
						"subtitle": "Liver Cancer Prediction",
						"buttons":[
							{
								"type":"web_url",
								"url": '',
								"title":"Liver Cancer Prediction"

							}
						]
					}
				]
			}
		}
	}
}
	elif payload == "DOCC":
		response_object = {
			"recipient":{
			"id":fbid
			},
			"message":{
				"attachment":{
				"type":"template",
				"payload":{
					"template_type":"generic",
					"elements":[
					{
						"title":"Dr Abhishek Gulia",
						"subtitle":"Radiation Oncology",
						"image_url":"https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.JONHpEjMoJ5k_GaosfCTMQDIB-%26pid%3D15.1&f=1",
						"buttons":[
							{
								"type":"web_url",
								"url":"",
								"title":"Max Hospital Delhi"
							}
						]
					},
					{
						"title":"Dr Akshay Tiwari",
						"subtitle":"Surgical Oncology",
						"image_url":"https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.JONHpEjMoJ5k_GaosfCTMQDIB-%26pid%3D15.1&f=1",
						"buttons":[
							{
								"type":"web_url",
								"url":"",
								"title":"Max Hospital Delhi"
							}
						]
					},
					{	
						"title":"Dr Shyam Aggarwal",
						"subtitle":"Medical Oncology",
						"image_url":"https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.vzXAYJf-XvT9ftMeiFqVMQDmCC%26pid%3D15.1&f=1",
						"buttons":[
							{
								"type":"web_url",
								"url":"",
								"title":"GangaRam Hospital Delhi"
							}
						]

					},
					{
						"title":"Dr S P Yadav",
						"subtitle":"Haemato Oncology",
						"image_url":"https://images.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.vzXAYJf-XvT9ftMeiFqVMQDmCC%26pid%3D15.1&f=1",
						"buttons":[
							{
								"type":"web_url",
								"url":"",
								"title":"GangaRam Hospital Delhi"
							}
						]
					},
					{

						"title":"Dr Lalit Kumar",
						"subtitle":"Medical Oncology",
						"image_url":"https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.nuttycloud.com%2Fwp-content%2Fuploads%2F2014%2F03%2FAIIMS-Logo-2014_Jodhpur.gif&f=1",
						"buttons":[
							{
								"type":"web_url",
								"url":"",
								"title":"All India Institute of Medical Sciences Delhi"
							}
						]
					}]
				}
				}
			}
		}

	elif payload == 'DONA':
		response_text = "Follow this link to give financial help to those in need https://1mp.me/donate"

	if response_text:s
		if response_object:
			response_object1 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
			response_object2 = json.dumps(response_object)
			requests.post(post_message_url, headers={"Content-Type":"application/json"}, data=response_object1)
			requests.post(post_message_url, headers={"Content-Type":"application/json"}, data=response_object2)
			return
		else:
			response_object = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
	else:
		response_object = json.dumps(response_object)
	status = requests.post(post_message_url, headers={"Content-Type":"application/json"}, data=response_object)
	logg(status.json(),symbol='----297----')
	return

def log(message):
	print (str(message))
	sys.stdout.flush()

if __name__ == '__main__':
	app.run(debug=True)	