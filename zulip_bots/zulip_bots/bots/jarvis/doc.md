# Jarvis
Jarvis is a Zulip bot that will help your workspace seach
for things on wikipedia, get learning courses in a click, 
get news relating to a given topic, analyse images and to
get some awful dad jokes. 
Responses are returned to the same stream they were @mentioned
in

We use a couple of API's (google, wikipedia, newsapi, dadjokes,
deepai) to obtain the required results

## Setup

Beyond the typical obtaining of the zuliprc file, no extra
setup is required to use the Jarvis Bot

## Usage

Using Jarvis is as simple as mentionong @\<jarvis-bot-name\>,
followed by a keyword:
@Jarvis wikipedia <Query>
@Jarvis analyse <image-url> 
@Jarvis teach_me <Topic Name> 
@Jarvis news <Topic>
@Jarvis joke

The command @\<jarvis-bot-name\> help gives a list of all possible 
commands that jarvis can handle 
