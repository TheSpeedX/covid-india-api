from flask import Flask , request
import json
from create_db import *
import sqlite3
from sqlite3 import Error
import re
import requests
import string
from datetime import datetime


app = Flask(__name__)
# PASSWORD="5tr0ng_P@ssW0rD"
PASSWORD="SpeedX"

@app.route('/')
def index():
	return """<html>
	<head><title>Corona India API | By SpeedX</title></head>
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000">
  <div class="centered-text"><h1><font color="#00ff00">
  <u>This is A Simple Corona Virus Infection in India API By SpeedX </u>
  </font></h1><br><br>
  <font color="#00ffff">
  <h3>
  <a href="/readme">Click Here</a> To go to the README Page
  </h3>
  </font><br><br><br>
  <h4><font color="#ff0000">
Made With ❤ By   <a href="mailto:ggspeedx29@gmail.com">SpeedX</a>
  </font></h4>
  </div></body></html>"""

@app.route('/update/'+PASSWORD)
def update():
	text=requests.get("https://www.mohfw.gov.in/").text
	statedata=text.split("<tr>")
	statedata=statedata[1:-2]
	conn=create_connection(database)
	clear_latest(conn)
	for state in statedata:
		data=re.findall(r"(?<=>)(.*)(?=<\/td>)",state)[1:]
		print(data)
		print("\n\n")
		update_state(conn,data[0],int(data[1])+int(data[2]),int(data[3]),int(data[4]))
	gen_new_report()
	URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}&as_occt=any&as_drrb=b&as_mindate={month}%2F%{from_day}%2F{year}&as_maxdate={month}%2F{to_day}%2F{year}&authuser=0'	
	cd = datetime.now().day
	cm = datetime.now().month
	response = requests.get(URL.format(query="Corona india", month=cm, from_day=cd, to_day=cd, year=20)).text

	filtered=response.split('<div class="kCrYT">')[1:-1]
	for x in range(0,len(filtered),2):
		link=(filtered[x][filtered[x].find("https://"):filtered[x].find("&amp;")])
		title=(filtered[x].split('</div>')[0].split('<div')[1].split('>')[1])
		update_news(title,link)
	return """
<html> 
<head> 
<title>Data Update | By SpeedX</title> 
<script language="JavaScript" type="text/javascript"> 
  
var seconds =6; 
// countdown timer. took 6 because page takes approx 1 sec to load 
  
var url="/"; 
  
function redirect(){ 
 if (seconds <=0){ 
  
  window.location = url; 
 } else { 
  seconds--; 
  document.getElementById("pageInfo").innerHTML="Redirecting to Home Page after <font color='#ff0000'><u>" 
+seconds+"</u></font> seconds." 
  setTimeout("redirect()", 1000) 
 } 
} 
</script> 
</head> 
  
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000" onload="redirect()">

  <div class="centered-text">
  <font color="#00ff00">
  <h4><p id="pageInfo"></p><h4>
  <h1>The Data Has Been Updated !!!</h1><br>
  <h3>
  <a href="/">Click Here</a> To go to the Home Page
  </h3>
  </font></div>
</html> 
	"""
@app.route('/api/state',methods=['POST'])
def state_stats():
	data=request.get_json()
	state=data['state']
	valid=string.ascii_letters+string.whitespace
	for s in state:
		if not s in valid:
			return json.dumps({"status":"failed"})
	return json.dumps(fetch_state(state))

@app.route('/api/news')
def news_stats():
	return json.dumps(fetch_news())

@app.route('/api/new')
def new_stats():
	return json.dumps(fetch_report())

@app.route('/api/total')
def total_stats():
	return json.dumps(fetch_total())

@app.route('/api/all')
def all_stats():
	return json.dumps(fetch_all())

@app.route('/api/guides')
def guides():
	return json.dumps('{"guides":[{"title":"How it Spreads?","link":"https://www.cdc.gov/coronavirus/2019-ncov/prepare/transmission.html","description":"Learn how Covid-19 spread"},{"title":"Symptoms","link":"https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html","description":"Learn how Covid-19 symptoms"},{"title":"Prevention & treatment","link":"https://www.cdc.gov/coronavirus/2019-ncov/prepare/prevention.html","description":"Learn Covid-19 treatments"},{"title":"What to do","link":"https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html","description":"What to do if you get the virus"}]}')

@app.route('/api/helpline')
def helpline():
	return json.dumps({'helpline':[{'state': 'Andhra Pradesh', 'phone': '0866-2410978'}, {'state': 'Arunachal Pradesh', 'phone': '9536055743'}, {'state': 'Assam', 'phone': '6913347770'}, {'state': 'Bihar', 'phone': '104'}, {'state': 'Chhattisgarh', 'phone': '077122-35091'}, {'state': 'Goa', 'phone': '104'}, {'state': 'Gujarat', 'phone': '104'}, {'state': 'Haryana', 'phone': '8558893911'}, {'state': 'Himachal Pradesh', 'phone': '104'}, {'state': 'Jharkhand', 'phone': '104'}, {'state': 'Karnataka', 'phone': '104'}, {'state': 'Kerala', 'phone': '0471-2552056'}, {'state': 'Madhya Pradesh', 'phone': '0755-2527177'}, {'state': 'Maharashtra', 'phone': '020-26127394'}, {'state': 'Manipur', 'phone': '3852411668'}, {'state': 'Meghalaya', 'phone': '9366090748'}, {'state': 'Mizoram', 'phone': '102'}, {'state': 'Nagaland', 'phone': '7005539653'}, {'state': 'Odisha', 'phone': '9439994859'}, {'state': 'Punjab', 'phone': '104'}, {'state': 'Rajasthan', 'phone': '0141-2225624'}, {'state': 'Sikkim', 'phone': '104'}, {'state': 'Tamil Nadu', 'phone': '044-29510500'}, {'state': 'Telangana', 'phone': '104'}, {'state': 'Tripura', 'phone': '0381-2315879'}, {'state': 'Uttarakhand', 'phone': '104'}, {'state': 'Uttar Pradesh', 'phone': '18001805145'}, {'state': 'West Bengal', 'phone': '3323412600'}, {'state': 'Andaman and Nicobar Islands', 'phone': '03192-232102'}, {'state': 'Chandigarh', 'phone': '9779558282'}, {'state': 'Dadra and Nagar Haveli and Daman &amp; Diu', 'phone': '104'}, {'state': 'Delhi', 'phone': '011-22307145'}, {'state': 'Jammu &amp; Kashmir', 'phone': '1912520982'}, {'state': 'Ladakh', 'phone': '1982256462'}, {'state': 'Lakshadweep', 'phone': '4896263742'}, {'state': 'Puducherry', 'phone': '104'}]})


@app.route('/api/predict',methods=['POST'])
def predict_stats():
	data=request.get_json()
	state=data['state']
	valid=string.ascii_letters+string.whitespace
	for s in state:
		if not s in valid:
			return json.dumps({"status":"failed"})
	return json.dumps(predict(state))

@app.route('/readme')
def readme():
	import markdown,tempfile,os
	text=open("README.md", encoding='utf-8')
	# md=markdown.markdown(text, safe_mode=False)
	stream= tempfile.TemporaryFile()
	markdown.markdownFromFile(input="README.md",output=stream)
	stream.seek(os.SEEK_SET)
	text=stream.read().decode()
	print(text)
	return """	<html> <head> <title>README | By SpeedX</title> </head> <body>"""+str(text)+"""</body></html>"""

@app.errorhandler(404) 
def not_found(e): 
	return """	
<html> 
<head> 
<title>Page Not Found</title> 
</head> 
  
	<style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            width: 100%;
        }
        body {
            display: table;
        }
        .centered-text {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }
        </style>
	<body style="background:#000000" onload="redirect()">

  <div class="centered-text">
  <font color="#00ff00">
  <h4><p id="pageInfo"></p><h4>
  <h1>Oops! Looks like you came the wrong way !!!</h1><br>
  <h3>
  <a href="/">Click Here</a> To go to the Home Page
  </h3>
  <h4>
  <a href="/readme">Click Here</a> To go to the README Page
  </h4>
  </font></div>
</html> 

"""	
app.run(debug=True)