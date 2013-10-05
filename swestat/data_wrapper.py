# -*- coding: utf-8 -*- 
"""
Provides functions to interact with the SCB web API by using simple 
HTTP GET messages
"""
import sys
import urlparse
import json
import urllib2
import pprint
import urllib

class MyError(Exception): 
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def get_url(url):
    try: 
        # send the request the easy way
        response = urllib2.urlopen(url)
        # check that the request was successfully processed
        status_code = response.getcode()
        if status_code != 200:
           raise MyError("Error at HTTP request. Error status: {}".\
                         format(status_code))
        # load result in json format 
        data = json.load(response)
        return data   
    except Exception, e:
        sys.exit(str(e))    


def main():
    url = "http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101A/BefolkningNy"
    #data = get_url(url)
    #pprint.pprint(data) 
    
    
    js = json.dumps({   
    "query": [
    {          
     "code": "ContentsCode",
     "selection": {         
     "filter": "item",         
     "values": [           
     "BE0101N1"         
    ]       
   }     
   },    
   {       
    "code": "Tid",
    "selection": {         
    "filter": "item",         
    "values": [           
    "2010",           
    "2011"         
    ]       
    }     
   }    
  ],   
  "response": {     
  "format": "csv",   
  } 
    })

    #data = urllib.urlencode(js)
    req = urllib2.Request("http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101A/BefolkningNy", js)
    response = urllib2.urlopen(req)
    print response.geturl()
    print response.info()
    print type(response)
    data = response.read()
    #for d in data:
    #  print d
    print data
    outf = open("XXX", "w")
    outf.write(data)
    outf.close()
    

if __name__ == "__main__":
    main()
