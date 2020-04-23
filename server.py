from flask import Flask , request, render_template, Markup
import json
from create_db import *
import sqlite3
from sqlite3 import Error
import re
import requests
import string
from datetime import datetime
import pickle
import os
import bs4

app = Flask(__name__)
# PASSWORD="5tr0ng_P@ssW0rD"
PASSWORD="SpeedXXX"

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
Made With ❤ By   <a href="https://github.com/TheSpeedX">SpeedX</a>
  </font></h4>
  </div></body></html>"""

@app.route('/update/'+PASSWORD)
def update():
	os.system('python3 dump.py &')
	maintext=requests.get("https://www.mohfw.gov.in/").text
	
	text=maintext[maintext.find('<div class="data-table table-responsive">'):maintext.find('<section id="site-advisories" class="site-update">')]
	statedata=text.split("<tr>")
	below_row=2
	statedata=statedata[2:-1-below_row]
	conn=create_connection(database)
	olddata=fetch_report()
	with open('data.dump', 'wb') as handle:
		pickle.dump(olddata, handle, protocol=pickle.HIGHEST_PROTOCOL)
	
	extradata={"info":None,"column":None,"dist_link":None}
	extradata['info']=re.findall(r"(?<=<strong>)(.*?)(?=<\/strong)",text.split('<tr>')[-1])[0]
	tmp=maintext[maintext.find('<div class="status-update">'):maintext.find('</div>',maintext.find('<div class="status-update">'))]
	extradata['timestamp']=tmp[tmp.find('<span>')+6:tmp.find('</span>')]
	# print(extradata['timestamp'])
	pdfs=re.findall(r"(https://www\.mohfw\.gov\.in/pdf/(.*)\.pdf)",maintext)
	for l,n in pdfs:
		if 'district' in n.lower():
			extradata['dist_link']=l
			break
		else:
			extradata['dist_link']=' '
	clear_latest(conn)
	pos=-1
	# print(statedata)
	notemark='*'
	for state in statedata:
		data=re.findall(r"(?<=>)(.*)(?=<\/td>)",state)[1:]
		ndata=[]
		for i,d in enumerate(data):
			if notemark in d:
				if '#' in d:
					d=d.replace('#','')
				d=d[:-1]
				pos=i
			ndata.append(d)
		data=ndata
		print(data)
		# print("\n\n")
		# update_state(conn,data[0],int(data[1])+int(data[2]),int(data[3]),int(data[4]))
		update_state(conn,data[0],int(data[1]),int(data[2]),int(data[3]))
	if pos==-1:
		ag=re.findall(r"(?<=<strong>)(.*?)(?=<\/strong)",text.split("<tr>")[-1])
		for i,d in enumerate(ag):
			if notemark in d:
				pos=i+1
	if pos==1 or pos==2:
		extradata['column']='T'
	elif pos==3:
		extradata['column']='R'
	elif pos==4:
		extradata['column']='D'
	else:
		extradata['column']=' '
	
	with open('stat.dump', 'wb') as handle:
		pickle.dump(extradata, handle, protocol=pickle.HIGHEST_PROTOCOL)
	data=re.findall(r"(?<=>)(\d+)(?=(<|\*))",text.split("<tr>")[-1-below_row])
	print(data)
	data=[ d[0] for d in data]
	# update_total(conn,int(data[0])-int(olddata["cases"]),int(data[1])-int(olddata["cured"]),int(data[2])-int(olddata["death"]))
	gen_new_report(data)
	# gen_new_report()
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

@app.route('/api/extras')
def extras():
	try:
		with open('stat.dump', 'rb') as handle:
			extradata = pickle.load(handle)
			return json.dumps(extradata)
	except:
		return json.dumps({"info":'',"column":'',"dist_link":'',"timestamp":''})
	
@app.route('/api/graphsvg/<param>')
def graphsvg(param):
	try:
		html=open("map.dump").read()
	except:
		return "<h1>Go Away!!</h1>"
	svg=html.split('<svg width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">')[1:]
	svgdata={"cases":None,"active":None,"cured":None,"death":None}
	for i,key in enumerate(svgdata):
		svgdata[key]='<svg width="100" height="100" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">'+svg[i][:svg[i].find('</svg>')+6]
	# print(svgdata)
	if param in svgdata.keys():
		return Markup(svgdata[param])
	else:
		return "<h1>Go Away!!</h1>"


@app.route('/india')
def india():
	prefix="""
	<html>
	<head>
	<title>Heatmap of India | By SpeedX </title>
	
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <!-- Bootstrap CSS -->
	
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
	</head>
	<body>
     <style>
      @import url('https://fonts.googleapis.com/css?family=Righteous&display=swap');
      </style>
	<script>
		function setdata(x)
		{
		document.getElementById("state").innerHTML=x
		}
		</script>
	<div class="jumbotron bg-transparent sm-12">
			<div class="row">
				<div class="col-sm-3">
					<div class="card bg-dark" align="center" id="state" style=" border: 1px #fff; border-radius: 20px; font-family: Righteous, cursive; color: #fff;">
					</div>
				</div>
	<div class="col-sm-9">
	"""
	suffix="""</div></div></div>
	
</body></html>"""
	html=open("map.dump").read()
	
	hindia='<svg id="chart" width="650" height="750" viewBox="0 0 450 450">'+html[html.find('<g class="india">')+17:]
	# hindia='<svg id="chart" width="650" height="750" viewBox="0 0 650 750">'+html[html.find('<svg id="chart" width="480" height="450" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid meet">')+99:]
	hindia=hindia[:hindia.find('</svg>')]+'</svg>'
	# hindia=hindia[:hindia.rfind('</g>')]+'</g></svg>'
	# print(hindia)
	soup = bs4.BeautifulSoup(prefix+hindia+suffix, 'html.parser') 
	g_container = soup.find('g', class_='states')  
	total=fetch_total()['cases']
	for ptag in g_container.find_all('path'):
		if 'Hello' in ptag.text:
			continue
		sd=ptag.text.split('from')[-1].strip()
		sp=sd.lower()
		data=fetch_state(sp)
		addon=''.join(["Total "+key+": "+str(data[key])+" <br>" for key in data])
		perc=round(data['cases']/total*100.0,2) if total!=0 else 0
		ptag['onclick'] = "setdata('{text}');".format(text=str("State: "+sd+"<br>"+addon+str(perc)+"% from "+string.capwords(sp)))
		ptag.string.replace_with(str(perc)+"% from "+string.capwords(sp))
	
	return Markup(str(soup))
@app.route('/world')
def world():
	return """
	<html>
	<head>
	</head>
	<body style="margin:0px;padding:0px;overflow:hidden">
    <iframe src="http://bing.com/covid" id="world" frameborder="0" style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:150%;width:150%;position:absolute;top:0px;left:0px;right:0px;bottom:0px" height="150%" width="150%"></iframe>
</body>
</html>
	"""

@app.route('/api/guides')
def guides():
	return json.dumps(json.loads('{"guides":[{"title":"How it Spreads?","link":"https://www.cdc.gov/coronavirus/2019-ncov/prepare/transmission.html","description":"Learn how Covid-19 spread"},{"title":"Symptoms","link":"https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html","description":"Learn Covid-19 symptoms"},{"title":"Prevention & treatment","link":"https://www.cdc.gov/coronavirus/2019-ncov/prepare/prevention.html","description":"Learn Covid-19 treatments"},{"title":"What to do","link":"https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html","description":"What to do if you get the virus"}]}'))

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
	# print(text)
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