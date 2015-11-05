#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import os
import base64
from sendEmail import sendEmail
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
httplib2.debuglevel = 1


def sendAPI(url):
    # we will totall try 3 times if send api fails
    retryCount = 3
    # set timeout 10s, over 10s, we assume it fails.
    http = httplib2.Http(timeout=10)
    email = "test@sensoro.com"
    password = "123456"
    auth = base64.encodestring(email + ':' + password)
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Cache-Control": "no-cache",
                "Authorization": "Basic " + auth,
                "Connection": "Keep-Alive",
                }
    while True:
        try:
            res, data = http.request(url, "GET", headers=headers)
            if not parseResponse(res):
                raise Exception("Response is not correct.")
            sleep(300)
        except Exception, e:
            if retryCount > 0:
                retryCount -= 1
                continue
            msg = "There is server API error. The URL is: %s.\r\n Exception is: %s." % (url, e)
            sendEmail(msg)
            sleep(3600)
            continue

def getApiList():
    try:
	path = os.getcwd()
        filePath = os.path.join(path, "get_api.txt")
        apiFile = open(filePath, "r")
        apiList = []
        for line in apiFile:
            apiList.append(line.strip())
        return apiList
    except Exception, e:
        print "Can not open get_api.txt file."
        print "Exception details: %s" % e

def parseResponse(response):
    if response['status'] == "200":
        return True
    else:
        return False

def main():
    apiList = getApiList()
    pool = ThreadPool(len(apiList))
    pool.map(sendAPI, apiList)
    pool.close()
    pool.join()

if __name__ == "__main__":
    # apiList = getApiList()
    # for i in apiList:
    #     print i
    # url = "http://www.sensoro.xxm/axc"
    # sendAPI(url)
    main()