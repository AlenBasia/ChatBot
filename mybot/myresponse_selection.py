"""
Response selection methods determines which response should be used in
the event that multiple responses are generated within a logic adapter.
"""
import logging
from mybot.mysql_storage import SQLStorageAdapter

def get_best_rated_response(input_statement, response_list, storage=None):
    '''
    Returns the response that is the best rated
    
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement

    :param response_list: A list of statement options to choose a response from.
    :type response_list: list

    :param storage: An instance of a storage adapter to allow the response selection
                    method to access other statements if needed.
    :type storage: StorageAdapter

    :return: Return the best rated statement in the response list.
    :rtype: Statement
    '''
    logger = logging.getLogger(__name__)
    logger.info('Selecting the best rated response from list of {} options.'.format(
        len(response_list)
    ))
    
    mystorage = SQLStorageAdapter()

    best_rate = -1

    # find the response with the best avg_rate
    for x in response_list:
        x_avg_rate = mystorage.getAvgRateById(x.id)

        if x_avg_rate > best_rate:
            response = x
            best_rate = x_avg_rate
    
    return response
