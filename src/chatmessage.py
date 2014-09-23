import time
class AllChat:
    def __init__(self):
        self.messages = []
    def addMessage(self, ide, name, message):
        self.messages.append(ChatMessage(ide, name, message))
    def getAllMessages(self):
        return self.messages
    def getRecentMessages(self):
        returns = []
        for x in self.messages[-1:0:-1]:
            if time.clock() - x.getTimeStamp() < 5:
                returns.append(x)
            else:
                break
        return returns
class ChatMessage:
    def __init__(self, ide, name, message, timestamp = time.clock()):
        self.message = message
        self.id = ide
        self.name = name
        self.timestamp = timestamp
    def getTimeStamp(self):
        return self.timestamp
    def getMessage(self):
        return self.message
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getJSON(self):
        return "{\"id\" : \"" + str(self.id) + "\", \"name\" : \"" + self.name + "\", \"message\" : \"" + self.message + "\"}"
