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

        if first_word == "wikipedia":
            bot_response = self.get_bot_wiki_response(message, bot_handler)
        elif first_word == "news":
            bot_response = self.get_bot_news(message,bot_handler)
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

    #def get_bot_joke_response(self, message: Dict[str, str], bot_handler: Any) -> Optional[str]:

    def get_bot_news(self, message, bot_handler: Any) -> Optional[str]:
        help_text = 'Please enter your search term after {}'

        # Checking if the link exists.
        query = message['content'][5:]
        if query == '':
            return help_text.format(bot_handler.identity().mention)

        query_news_url = 'https://newsapi.org/v2/everything?'
        query_news_params = dict(
            apiKey='e7682c2d3cd64221984d798bdc9dff4b',
            language='en',
            pageSize=3,
            q=query
        )
        try:
            data = requests.get(query_news_url,query_news_params)
        except requests.exceptions.RequestException:
            #logging.error('broken link')
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now. :slightly_frowning_face:\n' \
                   'Please try again later.'

        # Checking if the bot accessed the link.
        if data.status_code != 200:
            return 'Uh-Oh ! Sorry ,couldn\'t process the request right now.:slightly_frowning_face:\n' \
                   'Please try again later. '+str(data.status_code)

        new_content = 'For search term:' + query + '\n'

        # Checking if there is content for the searched term
        if len(data.json()['articles'])== 0:
            new_content = 'I am sorry. The search term you provided is not found :slightly_frowning_face:'

        else:
            for i in range(min(3,len(data.json()['articles']))):
                author = data.json()['articles'][i]['author']
                title = data.json()['articles'][i]['title']
                description = data.json()['articles'][i]['description']
                url = data.json()['articles'][i]['url']
                if author is None:
                    new_content += str(
                        i + 1) + ': Title: ' + title + '\n   ' + description + '\n (' + url + ') \n'
                else:
                    new_content += str(i+1) + ': Author: '+author+'\n   Title: '+title+'\n   '+description+'\n ('+url+') \n'
        return new_content


handler_class = JarvisHandler
