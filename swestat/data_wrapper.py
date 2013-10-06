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

def built_post_query(data):
    """ Given a table metadata built a json query to pull ALL the data """
    question = {}
    question['query'] = []
    for var in data['variables']:
        val = {}
        val['code'] = var['code']
        val['selection'] = {'filter' : 'all', 'values':['*']}
        question['query'].append(val)
    question['response'] = {'format': 'json'}
    return json.dumps(question)

"""
{ "query": [{"code":"Fodelseland", "selection":{"filter":"item", 
 "values":["010","020"]}}, 
 {"code":"Alder", "selection":{"filter":"all", "values":["*"]}}, 
 {"code":"Tid", "selection":{ "filter":"top", "values":["3"]}}], 
"response": {"format":"csv"} 
}
"""    

def pull_data(url):
   """ Given an URL including table metadata, get this metadata, then pull 
   all the data """
   # get the metadata of the table 
   table_meta_data = get_url(url)
   # build a json query to pool all the data
   json_query = built_post_query(table_meta_data) 
   # send a POST request 
   req = urllib2.Request(url, json_query)
   # get the response 
   response = urllib2.urlopen(req)
   data = response.read()
   return data    

def write_data2file(outfile, data):
    outf = open(outfile, "w")
    outf.write(data)
    outf.close()


def main():
    url = "http://api.scb.se/OV0104/v1/doris/en/ssd/BO/BO0201/BO0201A/KostnaderPerAreorFH2"
    data = pull_data(url)
    print data
    write_data2file("XXX", data)


if __name__ == "__main__":
    main()
