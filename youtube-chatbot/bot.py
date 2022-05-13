from auth import Oauth
from googleapiclient.discovery import build
import time
import random

file1 = open('liveChatId.txt', 'w')

authResponse = Oauth('client_secrets.json')
creds = authResponse.credentials

youtube = build(
    'youtube',
    'v3',
    credentials=creds
)

# Gets details of the currently active stream
stream = youtube.videos().list(
    part='snippet,liveStreamingDetails',
    id='pCatwMLP4BY'
)
response = stream.execute()
liveChatId = response['items'][0]['liveStreamingDetails']['activeLiveChatId']

file1.write(f'{liveChatId}')
file1.close()
file1 = open('liveChatId.txt', 'r')
for line in file1:
    print(line)
    liveChatId = line
file1.close()
print('LiveChatId')


def getUser(userId):
    channel = youtube.channels().list(
        part='snippet',
        id=userId
    )
    response = channel.execute()
    name = response['items'][0]['snippet']['title']
    return name


# Gets all the messages and their details from the live chat
'''1. Apparently links dont go through if you are not the owner
2. Make it so the bot replies to all the messages within the past 3 seconds'''
messagesList = []
totalruns = 0
while(True):
    print('sleeping')
    time.sleep(3)
    print('woke\n')
    notRead = []
    # if totalruns == 0:
    #     messages = youtube.liveChatMessages().list(
    #         liveChatId=liveChatId,
    #         maxResults=10,
    #         part='snippet'
    #     )
    # else:
    messages = youtube.liveChatMessages().list(
        liveChatId=liveChatId,
        part='snippet'
    )
    response = messages.execute()
    print('Fetch Complete\n')
    nextPageToken = response['nextPageToken']
    print('NPT:', nextPageToken)
    allResponses = response['items']
    if len(messagesList) == 0 and len(allResponses) > 0:
        for messages in allResponses:
            message = messages['snippet']['textMessageDetails']['messageText']
            userId = messages['snippet']['authorChannelId']
            messageTime = messages['snippet']['publishedAt']
            messagesList.append((messageTime, userId, message))

    else:
        for messages in allResponses:
            message = messages['snippet']['textMessageDetails']['messageText']
            userId = messages['snippet']['authorChannelId']
            messageTime = messages['snippet']['publishedAt']

            if (messageTime, userId, message) not in messagesList:
                notRead.append((messageTime, userId, message))
            if (messageTime, userId, message) not in messagesList:
                messagesList.append((messageTime, userId, message))
        print(notRead)

    # for the insertion of messages into the livechat
    for newMessages in notRead:
        Message = newMessages[-1]
        User = newMessages[1]
        name = getUser(User)
        if Message == "!bruh":
            insert = youtube.liveChatMessages().insert(
                part='snippet',
                body={"snippet": {
                    "liveChatId": liveChatId,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": f"{name} says bruh!"}}}
            )
            insert.execute()
            print('Message Replied!')

        elif Message == "!disc":
            url = 'https://discord.gg/mcBcaGg6'
            insert = youtube.liveChatMessages().insert(
                part='snippet',
                body={"snippet": {
                    "liveChatId": liveChatId,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": f"{url} here ya go join :)"}}}
            )
            insert.execute()
            print('Message Replied!')

        elif Message == "!rand":
            quotes = ['Why are these all dad jokes?',
                      'What’s brown and sticky? A stick.',
                      'Two guys walked into a bar. The third guy ducked.',
                      'How do you get a country girl’s attention? A tractor.',
                      'Why are elevator jokes so classic and good? They work on many levels.',
                      'What do you call a pudgy psychic? A four-chin teller.']
            message = random.choice(quotes)
            insert = youtube.liveChatMessages().insert(
                part='snippet',
                body={"snippet": {
                    "liveChatId": liveChatId,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": f'"{message}"'}}}
            )
            insert.execute()
            print('Message Replied!')

        totalruns += 1
