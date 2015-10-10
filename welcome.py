# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import random
from flask import Flask,request
from processFeed import processFeed
import prismatic

app = Flask(__name__)

@app.route('/')
def Welcome():
    print(request.args)
    twit = request.args.get("twitterHandle")
    if twit != None:
        print("Seeking topics for %s"%twit)
        try:
            res = processFeed(twit)
            lis = []
            if res is []:
                return None
            #print(json.dumps(res))
            topico = []
            for a in res:
                if type(a) is list:
                    for b in a:
                        if b[0] != u'@':
                            topico.append(b)
                else:
                    if a[0] != u'@':
                        topico.append(a)
                    
            topics = random.sample(topico, 3)
#            for i in topics:
#                if type(i) is list:
#                    for k in i:
#                        topico.append(k)
#                else:
#                    topico.append(i)
#            topics = topico
            print( "Picked out the topic set %s" % topics )
            json_dumps = []
            for topic in topics:
                tops = prismatic.getTopicByName( topic )
                print( "Result of topic name lookup is %s" %tops)
                if tops is not []:
                    topid = random.choice(tops)['id']
                    print( "Resolved topic %s to topic ID %i" % (topic,topid) )
                    art = prismatic.getArticlesByTopic( topid )
                    print( "Got articles %s" % art )
                    json_dumps.append(art)

                else:
                    continue
            return json.dumps(json_dumps)
        except Exception as e:
            print("something went wrong...")
            print(e)
            return None
    return app.send_static_file('index.html')

# randomly choose from nested lists until we're not dealing with a list
def randomChoice(l):
    if type(l) is not list:
        return l

    r = random.choice(l)
    if type(r) is list:
        return randomChoice(r)
    else:
        return r

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
