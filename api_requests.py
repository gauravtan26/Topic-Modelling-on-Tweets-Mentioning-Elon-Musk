import json
import pycurl
from io import BytesIO 
import os
import math
from datetime import datetime
import time

# rate cap for recent endpoint
# 450 requests/ 15 min per app
# 180 requests/ 15 min per user

wait_time = 2

######## REQUEST PARAMETERS ######

# use the twitter API tool to construct query strings easier. Refer https://developer.twitter.com/apitools/api?endpoint=%2F2%2Ftweets%2Fsearch%2Frecent&method=get
base_api_endpoint = "https://api.twitter.com/2/tweets/search/recent"

query_string = "query=(jlr%20OR%20jaguar%20OR%20landrover%20OR%20jaguarlandrover%20OR%20%23jlr%20OR%20%23jaguar%20OR%20%23landrover%20OR%20%23jaguarlandrover)%20lang%3Aen%20-is%3Aretweet"
                
query_params_dict = {
    "max_results" : "100", # enter number between 10 and 100
    "next_token" : {}
}

######## HEADERS ##########

# make a developer account on twitter and use the bearer token specified there
BEARER_TOKEN = ""

header = []
header.append("Authorization: Bearer " + BEARER_TOKEN)

#print(header)

######## FUNCTIONS ########

# appending tweets from each request/page to a master list
def appendTweets(json_object, tweetList):
    #print(type(json_object))
    tweets = json_object["data"]
    print("Tweets received from request : " + str(len(tweets)))
    for tweet in tweets:
        tweetList.append(tweet)
    #print(len(tweetList))

# request api for tweets
def getTweets(num_pages, tweetList):
    count = 0
    response_code = 0
    successes = 0

    start = time.time()

    while count < num_pages :
        request_URL = base_api_endpoint + "?" + query_string

        # concatenating all query params to request URL
        for param in query_params_dict:
            if(query_params_dict[param]):
                request_URL = request_URL + "&" + str(param) + "=" + query_params_dict[param]

        #print(request_URL)

        b_obj = BytesIO() 
        crl = pycurl.Curl()

        # Set URL value
        crl.setopt(crl.URL, request_URL)

        # add auth token to headers
        crl.setopt(crl.HTTPHEADER, header)

        # Write bytes that are utf-8 encoded
        crl.setopt(crl.WRITEDATA, b_obj)

        # spacing requests to obey rate cap
        if(count):
            time.sleep(wait_time)

        # sending http request
        try:
            print("Sending HTTP request " + str(count+1) + " .....") 
            crl.perform() 

            response_code = crl.getinfo(crl.RESPONSE_CODE)
        except:
            print("Pycurl error!!!")

        if(response_code==200):
            print("Successful request!")
            successes+=1

            # Get the content stored in the BytesIO object (in byte characters) 
            get_body = b_obj.getvalue()

            # Decode the bytes stored in get_body (a json object) into a dict and print the result 
            print("Parsing response.....")
            response_json = json.loads(get_body)
            #print(response_json)

            appendTweets(response_json, tweetList)

            # checking if metadata available
            if "meta" in response_json.keys():
                meta_dict = response_json["meta"]

                # api v2 uses pagination, require next_token to retrieve next page. Refer https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/paginate
                # checking if next_token available
                if "next_token" in meta_dict.keys():
                    query_params_dict["next_token"] = meta_dict["next_token"]
                else:
                    print("Tweets exhausted!!!")
                    query_params_dict["next_token"] = {}
                    break
            else:
                print("No metadata!!!")
                break
            
        else:
            print("Failed request!")
        
        # End curl session
        crl.close()

        count+=1

    end = time.time()
    job_time = end - start

    return(tweetList, query_params_dict["next_token"], successes, job_time)

######## MAIN #########
tweetList = []

NUM_TWEETS = 45000

num_pages = NUM_TWEETS/int(query_params_dict["max_results"])
#print(num_pages)

retrievedTweetObject = getTweets(num_pages, tweetList)
print("Number of retrieved tweets : " +str(len(retrievedTweetObject[0])))

print("-"*60)
print("JOB DETAILS :")
print("Successful requests : " + str(retrievedTweetObject[2]) + "/" + str(num_pages))
print("Time taken : " + str(retrievedTweetObject[3]))

# datetime object containing current date and time
now = datetime.now()

# formatting into file name
json_file = now.strftime("%d_%m_%Y_%H_%M_%S") + "_total_" + str(len(retrievedTweetObject[0])) + ".json"
#print(json_file)

#converting list to dict and storing as json file
dataStore = {}
dataStore["data"] = retrievedTweetObject[0]
dataStore["next_token"] = retrievedTweetObject[1]
dataStore["time"] = now.strftime("%d_%m_%Y_%H_%M_%S")

with open(json_file, "w") as outfile:
    json.dump(dataStore, outfile)
