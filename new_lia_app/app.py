from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

#LI-A application specific
API_KEY = "149yt4504foj"
SECRET_KEY = "V5149cV4nQyiDoF1"
SCOPE = "r_fullprofile r_network"
STATE = "sldkjfalksdfas"
REDIRECT_URI = "http://localhost:8000/auth"

@app.route("/")
def hello():
	url = """https://www.linkedin.com/uas/oauth2/authorization?response_type=code
											&client_id=%s
											&scope=%s
											&state=%s
											&redirect_uri=%s
											""" % (API_KEY, SCOPE, STATE, REDIRECT_URI)
	return render_template('index.html', url=url)


@app.route("/auth", methods = ["GET", "POST"])
def pullAuthoricationCodes():
	code = request.args.get("code")
	state = request.args.get("state")
	print "code", code
	print "State", state
	tokens_url = """https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s&client_secret=%s""" % (code, REDIRECT_URI, API_KEY, SECRET_KEY)
	print tokens_url
	r = requests.post(tokens_url)
	print "token url response", r.json()
	token = r.json()['access_token']

	people_url = "https://api.linkedin.com/v1/people/id=x0-DPtdArp/connections?oauth2_access_token=%s&format=json" %(token)
	people_search_url = "https://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,picture-url,headline),num-results)?oauth2_access_token=%s&format=json" %(token)
	r = requests.get(people_search_url)
	#num_connections = len(r.json()['values'])
	#print "number of connections", num_connections

	with open("data.txt", "w") as f:
		f.write(json.dumps(r.json()))

	return "GOT IT"



if __name__ == "__main__":
	app.debug = True
	app.run(port=8000)