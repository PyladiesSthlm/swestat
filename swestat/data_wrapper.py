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
import ast
import os
import matplotlib.pyplot as plt


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
   return ast.literal_eval(data)    

def write_data2file(outfile, data):
    outf = open(outfile, "w")
    outf.write(data)
    outf.close()

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def plot_data(labels, content_data, out_file, ylabel):
    time_data = [(int(labels[i]), float(content_data[i])) \
                  for i in range(0, len(content_data)) \
                  if isFloat(content_data[i])]
    time_data.sort(key = lambda p: p[0])    
    if len(time_data) < 7:
        print content_data
        return 
    plt.plot(range(0, len(time_data)), [d[1] for d in time_data], \
                 "b-", linewidth = 2.0)
    step = len(time_data) / 7
    plt.xticks(range(0, len(time_data), step), \
                   [str(time_data[j][0]) for j in range(0, len(time_data), step)])
    plt.ylabel(ylabel, fontsize = "20")
    plt.savefig(out_file+".pdf", format = "pdf")
    plt.close()


def plot_col_per_time(data, out_folder):
    """ Given a data dictionary, find if a period exists. If it does, then make plots 
    with all the columns of c type """
    i = 0
    t = 0 
    c = 0
    time_columns = []
    content_columns = []
    d_columns = []
    while i < len(data["columns"]):
        col = data["columns"][i]
        if "type" in col:
            if col["type"] == "t":
                time_columns.append((t, col["code"], col["text"]))
                t += 1
            elif col["type"] == "c":
                content_columns.append((c, col["code"], col["text"]))
                c += 1
            else:
                d_columns.append((t, col["code"], col["text"]))
                t += 1
        else:
            d_columns.append((t, col["code"], col["text"]))    
            t += 1
        i += 1
    print time_columns
    print content_columns
 
    # set the value of all the other d and t columns as the first value 
    set_cols = []
    for tup in time_columns[1:] + d_columns:
        v1 = data["data"][0]["key"][tup[0]]
        set_cols.append((tup[0], tup[1], tup[2], v1))

    filtered_data = []
    for d in data["data"]:
        corr = True
        for sc in set_cols:
            id = sc[0]
            v = sc[3]
            if d["key"][id] != v:
                corr = False
                break
        if corr:
            filtered_data.append(d)

    print filtered_data
    data  = filtered_data 


    i = time_columns[0][0]
    labels = [d["key"][i] for d in data]
    
    if len(time_columns) > 0 and len(content_columns) > 0:
        tcol = time_columns[0]
        i = 0
        while i < len(content_columns):
            outfile = os.path.join(out_folder, content_columns[i][1])
            j = content_columns[i][0]
            content_data = [d["values"][j] for d in data]
            plot_data(labels, content_data, outfile, content_columns[i][2])
            i += 1

        
    

    


def main():
    url = "http://api.scb.se/OV0104/v1/doris/en/ssd/BO/BO0201/BO0201A/KostnaderPerAreorFH2"
    data = pull_data(url)
    print type(data)
    for col in  data["columns"]:
        print col["text"], " ", col["type"] 
    print "-------------"
    plot_col_per_time(data, "figures")


    #print len(data['columns'])
    #write_data2file("XXX", data)


if __name__ == "__main__":
    main()
