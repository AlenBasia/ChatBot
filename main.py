from mybot.mychatterbot import ChatBot
from mybot.mysql_storage import SQLStorageAdapter
from chatterbot.trainers import ChatterBotCorpusTrainer
from mybot.myresponse_selection import get_best_rated_response

from flask import Flask, render_template, request, Markup, redirect, url_for, jsonify, session, redirect, url_for
import json

from admin.admins import Administration

import logging
from log.mylogger import *
import time

logging.basicConfig(level=logging.INFO)


def question_request(question):
    '''
    This function handles a question request from user
    :param question: A string with the quesstion
    Returns a list with 2 Statements [input_statement, output_statement]
    '''

    start = time.time()
    
    response = chatbot.get_response(question)

    end = time.time()
    elapsedTime = end - start

    #LOG TO FILES
    tolog = allLogs(response[0], response[1], elapsedTime)
    #if the answer is the default
    if response[1].id == None:
        tofailedlog = notAnsweredLogs(response[0])
    
    return response


def rating_request(myrate,response):
    '''
    This function handles a rating request from user
    :param myrate: An integer between 1 and 5
    :param response: A list with 2 Statements [input_statement, output_statement]
    Returns True if rating was successful.
    '''

    rated = False
    
    #if the answer is not the default
    if(response[1].id != None):
            
        #if rating is over 3 then learn
        if myrate > 3 and myrate < 6: 
            #save rating to the old statement
            chatbot.storage.updateRating(response[1].id,myrate)

            #response fix to save
            response[1].id = None

            #learn response
            '''chatbot.learn_response(response[0])'''
            chatbot.storage.create(**response[0].serialize())
            chatbot.storage.create(**response[1].serialize())
                
            #save rating to the new statement
            newid = chatbot.storage.count()
            chatbot.storage.updateRating(newid,myrate)

        elif myrate > 0:
            #save rating to the response
            chatbot.storage.updateRating(response[1].id,myrate)
            #LOG TO LOW RATED
            tolowratedlog = lowRatedLogs(response[0], response[1], response[1].id, myrate)
            
        rated = True

    else:
        print('Default Answer: Not saving response and rating!')


    return rated



######
#MAIN#
######

#create a bot
chatbot = ChatBot("MSc's Guru",
                  storage_adapter='mybot.mysql_storage.SQLStorageAdapter',
                  preprocessors=['mybot.mypreprocessors.final_sigma','chatterbot.preprocessors.clean_whitespace','mybot.mypreprocessors.remove_questionmark'],
                  logic_adapters=[
                {
                    'import_path': 'mybot.mybest_match.BestMatch',
                    'response_selection_method': get_best_rated_response,
                    'default_response': "Συγνώμη δεν σας καταλαβαίνω. Δοκιμάστε να διατυπώσετε την ερώτησή σας με διαφορετικό τρόπο."
                }
                ],
                  read_only = True
                  ) 



#train the bot if there are no records at the storage
if chatbot.storage.count()<1:
    #create a trainer
    trainer = ChatterBotCorpusTrainer(chatbot)

    #train with the training files
    trainer.train(
        "trainingfiles.humanize","trainingfiles.humanize2","trainingfiles.info","trainingfiles.info2","trainingfiles.classes","trainingfiles.classes2","trainingfiles.communication","trainingfiles.communication2"
    )

    #the weights after training need to be maximum
    #update all weights to max
    for i in range(1,chatbot.storage.count()+1):
        chatbot.storage.setMaxWeight()

#Chatting Data
texts = []

#UserInterface
app = Flask(__name__)
app.secret_key = 'autoeinaigiatasessionskaiprepeinaeinaikrufo'

#home route
@app.route("/")
def home():
    return render_template("index.html")

#JsonRequests
@app.route('/processjson', methods=['POST'])
def processJson():
    #get data
    data = request.get_json()
    typeOfRequest = data['type'] #type of request question | rating
    inputRequest = data['input'] #input value
    inputID = data['id'] #if user rated there will be an id of the answer he rated
    myresponse = "None"
    myid = -1 
    #if user submitted question
    if typeOfRequest == "question":
        #generate response
        response = question_request(inputRequest)
        #add userinput and response to texts
        texts.append(response)
        #get the index of last item in texts
        myid = len(texts)-1
        myresponse = Markup(response[1])
    elif typeOfRequest == "rating":
        myresponse = rating_request(int(inputRequest),texts[int(inputID)])
        myid = inputID
    
    return json.dumps({'response':myresponse,'id':myid}), 200, {'ContentType':'application/json'}

#ADMIN SECTION
alladmins = []
alladmins.append(Administration(user='admin',passw='admin'))

@app.route("/admin")
def admin():
    if not session.get('user'):
        return redirect(url_for('login'))
    data = chatbot.storage.getAllAnswers()
    data_less = chatbot.storage.getAllAnswersLess()
    return render_template("admin.html", less=data_less,data=data)
    
@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route('/userauth', methods=['POST'])
def userauth():
    
    session.pop('user', None)
    
    #get data
    data = request.get_json()
    typeOfRequest = data['type'] #type of request auth
    user = data['user'] #username
    passw = data['passw'] #password
    
    #check if user exists and has that passw
    isuser = [i for i in alladmins if i.user == user][0]
    if isuser and isuser.passw==passw:
        session['user']=isuser.user
        return json.dumps({'login': True}), 200, {'ContentType':'application/json'}
    
    return json.dumps({'login': False}), 200, {'ContentType':'application/json'}
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'), code=302)
    
#JsonUpdateRequest from an admin
@app.route('/updatejson', methods=['POST'])
def updatejson():
    #get data
    data = request.get_json()
    typeOfRequest = data['type'] #type of request update
    old = data['old'] #old text
    ID = data['id'] #id of the text in db
    changeall = data['all'] #replace all related
    new = data['newtext'] #new text
    if changeall:
        chatbot.storage.replaceAllAnswers(old, new)
    else:
        chatbot.storage.replaceAnswersByID(ID, new)
    
    
    return json.dumps({'response': True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run()


'''
#PythonConversation
while True:
    try:

        #Get request
        request = input('You: ')

        #Get response
        response = question_request(request)
        print('Bot: ',response[1])

        #Get rating
        myrate = int(input('Rate: '))

        #Handle Rating
        rated = rating_request(myrate,response)
        
                
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
'''
