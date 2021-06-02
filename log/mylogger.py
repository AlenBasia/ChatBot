from datetime import datetime

"""
These functions are used to create log files and append them
"""

def allLogs(userinput, response):
    """
    This function is used to log the users' inputs and the responses they get.
    A file is created or if exists appends it.

    :param userinput:
        The user's input
    :type userinput: string

    :param response:
        The response that the user got
    :type response: string
    """
    line = "Time: {}    ||  Input: {}   ||  Response: {}\n\n".format(datetime.now(),userinput, response)
    try:
        with open("log/dialogs.log", 'a') as file:
            file.write(line)
            return 0
    except IOError:
        print("Could not open 'dialogs.log'\n Line lost: ", line)
    return 1

def notAnsweredLogs(userinput):
    """
    This function is used to log the inputs that failed to get an answer.
    A file is created or if exists appends it.

    :param userinput:
        The user's input
    :type userinput: string
    """
    line = "Time: {}    ||  Input: {}\n\n".format(datetime.now(),userinput)
    try:
        with open("log/failed.log", 'a') as file:
            file.write(line)
            return 0
    except IOError:
        print("Could not open 'failed.log'\n Line lost: ", line)
    return 1

def lowRatedLogs(userinput, response, responseId, rating):
    """
    This function is used to log the responses that got low rating.
    A file is created or if exists appends it.

    :param userinput:
        The user's input
    :type userinput: string

    :param response:
        The response that the user got
    :type response: string

    :param responseId:
        The response's Id on the Database
    :type responseId: integer

    :param rating:
        The rating that the response got.
    :type rating: integer
    """
    line = "Time: {}    ||  Input: {}   ||  Response: {}    ||  ResponseID: {}  ||  Rating: {}\n\n".format(datetime.now(),userinput, response, responseId, rating)
    try:
        with open("log/lowrated.log", 'a') as file:
            file.write(line)
            return 0
    except IOError:
        print("Could not open 'lowrated.log'\n Line lost: ", line)
    return 1

