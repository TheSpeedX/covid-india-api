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
  <h2><font color="#00ffff">For usage Mail SpeedX: 
  <a href="mailto:ggspeedx29@gmail.com">ggspeedx29[at]gmail[dot]com</a>
  </font></h2>
  </div></body></html>"""

@app.route('/update/'+PASSWORD)
def update():
	text=requests.get("https://www.mohfw.gov.in/").text
	statedata=text.split("<tr>")
	statedata=statedata[1:-1]
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
	return json.dumps({"report":fetch_report()})

@app.route('/api/total')
def total_stats():
	return json.dumps(fetch_total())

@app.route('/api/all')
def all_stats():
	return json.dumps(fetch_all())


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