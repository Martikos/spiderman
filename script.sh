# curl -H "Accept:application/json" -H "Content-type:application/json" -X POST -d '{ "ads": [{ "channelName": "", "creatives": [], "description_1": "", "description_2": "", "destinationURL": "http:www.url.com", "displayURL": "www.url.com", "headline": "", "id": 1, "media_id": "", "name": "My Ad [11-13 2:40]", "templateAdCreatives": "InStreamVideoDisplay.html", "type": "INSTREAM", "videoSourceURL": "http://youtu.be/F2zTd_YwTvo" }], "budget": 10, "endDate": "11-15-2013", "bidStrategies": [ { "type": "CPC", "value": "" }, { "type": "CPM", "value": 1.25} ], "videoSetID": "52546cb0bd592a1999d1d1b4", "maxCPC": "", "maxCPM": 1, "maxDailyBudget": 5, "name": "My Campaign [11-13 2:40]", "objective": "impressions", "startDate": "11-13-2013", "tier": "BRAND_TARGETED" }' http://localhost:5000/
curl -H "Accept:application/json" -H "Content-type:application/json" -X POST -d '{ "function": "expand", "input": { "seed": ["A3PDXmYoF5U"] }, "count": 100, "identifier": "123" }' http://localhost:5000/