# COVID-INDIA-API
A Web API To Get Details of Corona in India

## Description
This is a Web API that Gets you Details of Corona Virus in India.
<br>
Like: 
<ul type="disc">
<li>Stats</li>
<li>News</li>
<li>New Cases</li>
<li>Prediction</li>
</ul>

### Starting Server

Start Server:
```python3 server.py```

#### To Get All States Statistics
Send A GET Request To ```http://domain.com/api/all```

#### To Get A recent news
Send A GET Request To ```http://domain.com/api/news```

#### To Update The Details
Send A GET Request To ```http://domain.com/update/{password}```

#### To Get A recent Reports After Update
Send A GET Request To ```http://domain.com/api/new```

#### To Get A State's Statistics
Send A POST Request To ```http://domain.com/api/state```
<br>
With The JSON data format: ```{"state":"statename"}```

#### To Get A State's Prediction of Getting Ill
Send A POST Request To ```http://domain.com/api/predict```
<br>
With The JSON data format: ```{"state":"statename"}```

### Valid State Names

Andhra Pradesh <br>
Delhi <br>
Haryana <br>
Karnataka <br>
Kerala <br>
Maharashtra <br>
Odisha <br>
Pondicherry <br>
Punjab <br>
Rajasthan <br>
Tamil Nadu <br>
Telengana <br>
Union Territory of Jammu and Kashmir <br>
Union Territory of Ladakh <br>
Uttar Pradesh <br>
Uttarakhand <br>
West Bengal <br>
Union Territory of Chandigarh <br>

#### Credits
Made With ❤ By SpeedX 
