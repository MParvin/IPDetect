#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 23:49:05 2018

@author: mparvin
"""
#ipDB = "/home/mparvin/Documents/MyGit/Flask/IP/ip.db"
ipDB = "./ip.db"

from flask import request
from flask import jsonify
import sqlite3 as sql3
import ipcalc
from flask import Flask

app = Flask(__name__)

### Detect IP is in Network
def isInNetwork(ipAddr, networkSubnet):
	# Detecting IP
	# '82.99.244.203' in ipcalc.Network('82.99.244.200/29')
	# True
	if ipAddr in ipcalc.Network(networkSubnet):
		return True
	else:
		return False

### Detecting IP and Return answer to User
def iDetect(exType):
    userIP = request.remote_addr
    try:
        # First get two first octed of IP
        firstOcted = '.'.join(userIP.split('.')[0:2])
        # Second query in database for IP's like this
        conn = sql3.connect(ipDB)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM ip_list WHERE ip LIKE "%s%"'''.format(firstOcted))
        dbRows = cur.fetchall()

        for singleRow in dbRows:
            # Thirs check with isInNetwork function
            ipNetwork = singleRow['ip']
            if isInNetwork(userIP, ipNetwork):
                if exType == 1:
                    return jsonify({'ip': userIP, 'continent': singleRow['continent'],'country': singleRow['country']}), 200
                return """%s,%s,%s""".format(userIP, singleRow['continent'], singleRow['country'])
        if exType == 1:
            return jsonify({'error': 'Cannot find IP'}), 300
        return "Cannot find IP in our Database"
    except 	sql3.Error as e:
        errorMessage = """There is error in database {}""".format(e)
        return errorMessage


### Routes
@app.route('/')
def getIP():
	return iDetect(0)

@app.route('/json')
def geJSONIP():
	return iDetect(1)

if __name__ == '__main__':
	app.run(debug=True)


