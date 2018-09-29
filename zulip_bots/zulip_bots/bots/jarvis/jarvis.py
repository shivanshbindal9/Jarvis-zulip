import requests
import logging
import re
import urllib
from zulip_bots.lib import Any

from typing import Optional, Any, Dict

# See readme.md for instructions on running this code.

class JarvisHandler(object):
    '''
    This plugin facilitates searching Wikipedia for a
    specific key term and returns the top 3 articles from the
    search. It looks for messages starting with '@mention-bot'

    In this example, we write all Wikipedia searches into
    the same stream that it was called from, but this code
    could be adapted to write Wikipedia searches to some
    kind of external issue tracker as well.
    '''

    def usage(self) -> str:
        return '''
            This plugin will allow users to directly search
            Wikipedia for a specific key term and get the top 3
            articles that is returned from the search. Users
            should preface searches with "@mention-bot".
            @mention-bot <name of article>'''

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:

        first_word = message['content'].split(' ', 1)[0]
        if first_word == "joke":
            bot_response = self.get_bot_joke_response(message,bot_handler)
        if first_word == "wikipedia":
            bot_response = self.get_bot_wiki_response(message, bot_handler)
        if first_word == "teach_me":
            bot_response = self.get_bot_teach_response(message, bot_handler)
        else:
            bot_response = self.get_bot_reply(message, bot_handler)
        bot_handler.send_reply(message, bot_response)



    def get_bot_wiki_response(self, message: Dict[str, str], bot_handler: Any) -> Optional[str]:
        '''This function returns the URLs of the requested topic.'''

        help_text = 'Please enter your search term after {}'

        # Checking if the link exists.
        query = message['content'][10:]
        if query == '':
            return help_text.format(bot_handler.identity().mention)

        query_wiki_url = 'https://en.wikipedia.org/w/api.php'
        query_wiki_params = dict(
            action='query',
            list='search',
            srsearch=query,
            format='json'
        )
        try:
            data = requests.get(query_wiki_url, params=query_wiki_params)

        except requests.exceptions.RequestException:
            logging.error('broken link')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'

        # Checking if the bot accessed the link.
        if data.status_code != 200:
            logging.error('Page not found.')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'

        new_content = 'For search term:' + query + '\n'

        # Checking if there is content for the searched term
        if len(data.json()['query']['search']) == 0:
            new_content = 'I am sorry. The search term you provided is not found :slightly_frowning_face:'
        else:
            for i in range(min(3, len(data.json()['query']['search']))):
                search_string = data.json()['query']['search'][i]['title'].replace(' ', '_')
                url = 'https://en.wikipedia.org/wiki/' + search_string
                new_content += str(i+1) + ':' + '[' + search_string + ']' + '(' + url.replace('"', "%22") + ')\n'
        return new_content

    def get_bot_joke_response(self, message: Dict[str, str], bot_handler: Any) -> Optional[str]:
        '''This function returns the URLs of the requested topic.'''

        help_text = 'Please enter your search term after {}'

        # Checking if the link exists.

        query_wiki_url = 'https://icanhazdadjoke.com/'
        
        try:
            data = requests.get(query_wiki_url, headers={"Accept":"application/json"})

        except requests.exceptions.RequestException:
            logging.error('broken link')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'

        # Checking if the bot accessed the link.
        if data.status_code != 200:
            logging.error('Page not found.')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'


        # Checking if there is content for the searched term
        if len(data.json()['joke']) == 0:
            new_content = 'I am sorry. The search term you provided is not found :slightly_frowning_face:'
        else:
            new_content = data.json()['joke']
        return new_content


    def get_bot_teach_response(self, message, bot_handler: Any) -> Optional[str]:
        '''This function returns the URLs of the requested topic.'''

        help_text = 'Please enter your search term after {}'

        # Checking if the link exists.
        query = message['content'][8:]
        if query == '':
            return help_text.format(bot_handler.identity().mention)

        query_wiki_url = 'https://www.googleapis.com/customsearch/v1'
        query_wiki_params = dict(
            key = 'AIzaSyDWus4C1ykIrL3q7uIYB1MCTIwdM5wfQDo',
            cx = '004985854750889686468:okdojnlvqsw',
            q=query,
           
        )
        try:
            data = requests.get(query_wiki_url, params=query_wiki_params)

        except requests.exceptions.RequestException:
            logging.error('broken link')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'

        # Checking if the bot accessed the link.
        if data.status_code != 200:
            logging.error('Page not found.')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later.'

        new_content = 'For search term:' + query + '\n'

        # Checking if there is content for the searched term
        if data.json()['queries']['request'][0]['count'] == 0:
            new_content = 'I am sorry. The search term you provided is not found :slightly_frowning_face:'
        else:
            for i in range(min(3, data.json()['queries']['request'][0]['count'])):
                result_title = data.json()['items'][i]['title']
                url = data.json()['items'][i]['link']
                snippet = data.json()['items'][i]['snippet']

                new_content += 'Title' + ':' + result_title + '\n' + 'Link' + ':' + url + '\n' \
                 + 'Description:' + snippet +  '\n' + '\n'
        return new_content

    def get_bot_reply(self, message, bot_handler: Any) -> Optional[str]:
        
        new_content = "It is not a valid query \n please check '@jarvis help'"
        return new_content



handler_class = JarvisHandler
