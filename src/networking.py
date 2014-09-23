import SocketServer, ast, chatmessage, mysql.connector, time, lobby, hero
from globalvars import *
class Header:
    def __init__(self, clientID, reqtype):
        self.clientID = clientID
        self.reqtype = reqtype
    def getClientID(self):
        return self.clientID
    def getReqType(self):
        return self.reqtype
    def toString(self):
        return "{\"clientID\" : \"" + str(self.clientID) + "\", \"reqtype\" : \"" + self.reqtype + "\"}"
class DataFrame:
    def __init__(self, header, d = {}):
        self.dict = d
        self.header = header
    def toString(self):
        string = "{"
        if len(self.dict) > 0:
            for key in self.dict:
                if type(self.dict[key]) == list:
                    string += "\"" + str(key) + "\" : " + str(self.dict[key]) + ","
                else:
                    string += "\"" + str(key) + "\" : \"" + str(self.dict[key]) + "\","
            string = string[0:-1]
        string += "}"
        return "{\"header\" : " + self.header.toString() + ", \"data\" : " + string + "}"
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def handle(self):
        print "got request"
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        try:
            d = ast.literal_eval(self.data)
            conHeader = Header(d["header"]["clientID"], d["header"]["reqtype"])
            if conHeader.reqtype == "fetchLobbies":
                self.request.sendall(DataFrame(Header(0, "sendLobbies"), self.getLobbyData()).toString())
            if conHeader.reqtype == "sendChat":
                self.sendChatData(chatmessage.ChatMessage(d["data"]["id"], d["data"]["name"], d["data"]["message"]))
                self.ac.addMessage(d["data"]["id"], d["data"]["name"], d["data"]["message"])
                self.request.sendall(DataFrame(Header(0, "recievedChat"), {}).toString())
            if conHeader.reqtype == "recvChat":
                c = self.getRecentChatData()
                self.request.sendall(DataFrame(Header(0, "sendRecentChat"), c).toString())
            if conHeader.reqtype == "registerAccount":
                if not self.registerAccount(d["data"]):
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "success")).toString())
            if conHeader.reqtype == "login":
                self.request.sendall(self.login(d["data"]))
            if conHeader.reqtype == "createLobby":
                if self.createLobby(d["data"]):
                    self.request.sendall(DataFrame(Header(0, "success")).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "challenge":
                playerID, jsons = self.challenge(d["data"])
                if len(jsons) > 0:
                    self.request.sendall(DataFrame(Header(0, "heroes"), {"playerID": playerID, "heroes" : jsons}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "checkForChallenge":
                self.request.sendall(self.checkChallenge(d["data"]))
            if conHeader.reqtype == "deleteLobby":
                self.request.sendall(self.deleteLobby(d["data"]))
            if conHeader.reqtype == "createHero":
                heroID = self.createHero(d["data"])
                if heroID:
                    self.request.sendall(DataFrame(Header(0, "success"), {"heroID" : str(heroID)}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "getHeroes":
                playerID, jsons = self.getHeroes(d["data"])
                if len(jsons) > 0:
                    self.request.sendall(DataFrame(Header(0, "heroes"), {"playerID": playerID, "heroes" : jsons}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "createMatch":
                if self.createMatch(d["data"]):
                    self.request.sendall(DataFrame(Header(0, "success")).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "connectToGame":
                gameID, playerID, jsons = self.connectToGame(d["data"])
                if len(jsons) > 0:
                    self.request.sendall(DataFrame(Header(0, "success"), {"gameID": str(gameID), "playerID" : playerID, "heroes" : jsons}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "sendTileChoice":
                if self.sendTileChoice(d["data"]):
                    self.request.sendall(DataFrame(Header(0, "success")).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())    
        except ValueError:
            pass
    def sendTileChoice(self, data):
        playerID = data["id"]
        row = data["row"]
        col = data["col"]
        heroID = str(data["hero"])
        gameID = data["gameID"]
        payload = "update currentgametiles set heroID="+heroID+" where hexColumn="+str(col)+" and hexRow=" +str(col)+" and GameID=" +str(gameID)+ ";"
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        cnx.commit()
        return 1
    def connectToGame(self, data):
        playerID = data["playerID"]
        
        payload = "select id, player2 from currentgames where player1 = "+playerID+";"
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        playerid = 0
        for gameID, ide in c:
            playerid = ide
            gameID = gameID
        print "CONNECT TO GAME TEST :::" + str(gameID) + " :: " + str(playerid)
        ide, jsons = self.getHeroes({"playerID" : playerid})
        return gameID, playerid, jsons 
    def getHeroes(self, data):
        playerID = data["playerID"]
        payload = "select * from heroes where playerID = " + str(playerID) + ";"
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        jsons = []
        for hero in self.makeHeroes(c):
            jsons.append(hero.getJSON())
        return playerID, jsons
    def makeHeroes(self, cursor):
        heroes = []
        for heroID, name, level, exp, stre, agi, con, wis, inte, hp, mana, currenthp, currentmana, meleeEquipment, rangedEquipment, armorEquipment, shieldEquipment, playerID, race, activeClass in cursor:
            h = hero.Hero(heroID, name, CLASSES[activeClass], RACES[race])
            h.level = level
            h.exp = exp
            h.strength = stre
            h.agi = agi
            h.con = con
            h.wis = wis
            h.inte = inte
            h.playerID = playerID
            h.maxhp = hp
            h.maxMana = mana
            h.currenthp = currenthp
            h.currentMana = currentmana
            h.meleeWeapon = MELEE_WEAPONS[meleeEquipment]
            h.rangedWeapon = RANGED_WEAPONS[rangedEquipment]
            h.armor = ARMOR[armorEquipment]
            h.shield = SHIELDS[shieldEquipment]
            h.race = RACES[race]
            h.activeHeroClass = CLASSES[activeClass]
            heroes.append(h)
        return heroes
    def createMatch(self, data):
        print data
        ID = data["gameID"]
        player1 = data["player1"]
        player2 = data["player2"]
        rows = int(data["rows"])
        cols = int(data["cols"])
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        for co in range(cols):
            for r in range(rows):
                payload = "insert into currentgametiles (gameID, hexColumn, hexRow) values ("+ID+", "+str(co)+", "+str(r)+");"
                c.execute(payload)
                cnx.commit()
        payload = "insert into currentgames (id, player1, player2) values ("+ID+", "+player1+", "+player2+");"
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
        return 1
    def createHero(self, data):
        playerid = data["playerID"]
        hero = data["hero"]
        hero = ast.literal_eval(hero)
        payloadHeader = "insert into heroes (playerID, "
        payloadData = ") values (" + str(playerid) + ", "
        for key in hero:
            if key == "name":
                payloadHeader += str(key) + ", "
                payloadData += "\"" + str(hero[key]) + "\", "
            elif key == "heroID":
                pass
            else:
                payloadHeader += str(key) + ", "
                payloadData += str(hero[key]) + ", "
        payloadHeader = payloadHeader[0:len(payloadHeader)-2]
        payloadData = payloadData[0:len(payloadData)-2]
        payload = payloadHeader + payloadData + ");"
        print payload
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        cnx.commit()
        payload = "select heroID from heroes where playerID = " + str(playerid) + ";"
        c.execute(payload)
        currhero = 0
        for heroID in c:
            print heroID[0]
            if int(heroID[0]) > currhero:
                currhero = heroID[0]
        return currhero
    def checkChallenge(self, data):
        print data
        playerid = data["id"]
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select * from lobbies where player1="+str(playerid)+";")
        c.execute(payload)
        for ide, player1, player2 in c:
            if player2 != None:
                return DataFrame(Header(0, "playerFound"), {"id" : player2}).toString()
        c.close()
        cnx.close()
        return DataFrame(Header(0, "failed")).toString()
    def deleteLobby(self, data):
        playerid = data["id"]
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("delete from lobbies where player1="+str(playerid)+";")
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
        return DataFrame(Header(0, "success")).toString()
    def challenge(self, data):
        lobbyid = data["lobby"]
        playerid = data["id"]
        print lobbyid, playerid
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("update lobbies set player2=" + str(playerid) + " where id = "+str(lobbyid)+";")
        c.execute(payload)
        cnx.commit()
        payload = "select player1 from lobbies where id=" + str(lobbyid) + ";"
        c.execute(payload)
        jsons = []
        for player1 in c:
            payload = "select * from heroes where playerID = "+ str(player1[0])+";"
            c.execute(payload)
            for hero in self.makeHeroes(c):
                jsons.append(hero.getJSON())
                
            
        c.close()
        cnx.close()
        return player1[0], jsons
    def levelUp(self, data):
        pass
    def createLobby(self, data):
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select * from lobbies where player1 = "+data["id"]+";")
        c.execute(payload)
        for x in c:
            return 0
        payload = ("insert into lobbies (player1) values(\""+ data["id"]+"\")")
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
        return 1

    def login(self, data):
        returnVal = DataFrame(Header(0, "failed"), {"reason": "Bad username or password"}).toString()
        name = data["name"]
        loginpassword = data["password"]
        print "Attempting to login with: " + name + " : " + loginpassword
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select id, username, password from accounts;")
        c.execute(payload)
        for ide, username, pas in c:
            if username == name and pas == loginpassword:
                returnVal = DataFrame(Header(0, "success"), {"id" : ide, "username" : username}).toString()
        c.close()
        cnx.close()
        return returnVal
    def registerAccount(self, data):
        name = data["name"]
        password = data["password"]
        print password
        print "Attempting to register: " + name + " : " +  password
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select username, password from accounts;")
        c.execute(payload)
        for username, p in c:
            if username == name:
                return 0
        payload = ("insert into accounts " +
                   "(username, password) "
                   "values (\"" + name + "\", \"" + password + "\");")
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
        return 1
    def sendChatData(self, message):
        pass
    def getRecentChatData(self):
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select messageid, name, message from AllChat where timestamp > " + str(int(time.clock())-10) + ";")
        c.execute(payload)
        chats = {}
        for ide, name, message in c:
            chats[ide] = chatmessage.ChatMessage(ide, name, message).getJSON()
        if len(chats) == 0:
            chats = None
        c.close()
        cnx.close()
        return chats
    def clearAllChat(self):
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("delete from AllChat;")
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
    def sendToAllSockets(self):
        pass
    def getLobbyData(self):
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = ("select id, player1, player2 from lobbies;")
        c.execute(payload)
        chats = {}
        lobbies = []
        for ide, player1, player2 in c:
            if player2 == None:
                lobbies.append((ide, player1))
        players = []
        for x in lobbies:
            payload = ("select username from accounts where id = " + str(x[1]) + ";")
            c.execute(payload)
            for username in c:
                print username
                players.append(username[0])

        l = []
        for x in range(len(lobbies)):
            l.append(lobby.Lobby(lobbies[x][0], players[x]))
        c.close()
        cnx.close()
        print l
        return {"lobbyCount" : len(l), "lobbies" : [x.toString().encode('ascii','ignore').replace("'", "") for x in l]}
        # just send back the same data, but upper-cased

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
