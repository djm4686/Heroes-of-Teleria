import SocketServer, ast, chatmessage, time, lobby, hero
from globalvars import *
if __name__ == "__main__":
    import mysql.connector
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
        self.DataFrameFactory = lambda header, data: DataFrame(Header(0, header), data).toString()
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def sendSQLPost(self, payload):
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        cnx.commit()
        c.close()
        cnx.close()
    def handle(self):
        print "got request"
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096).strip()
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
                data = self.connectToGame(d["data"])
                if data != None:
                    self.request.sendall(DataFrame(Header(0, "success"), {}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "testConnectToGame":
                gameID, playerID, jsons = self.testConnectToGame(d["data"])
                print "connect to game response: {}, {}, {}".format(gameID, playerID, jsons)
                if len(jsons) > 0:
                    self.request.sendall(DataFrame(Header(0, "success"), {"gameID" : str(gameID), "playerID" : playerID, "heroes" : jsons}).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "sendTileChoice":
                if self.sendTileChoice(d["data"]):
                    self.request.sendall(DataFrame(Header(0, "success")).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "askForBoard":
                data = self.askForBoard(d["data"])
                if len(data) > 0:
                    self.request.sendall(DataFrame(Header(0, "success"), data).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "nextTurn":
                data = self.nextTurn(d["data"])
                if len(data) > 0:
                    self.request.sendall(self.DataFrameFactory("success", data))
                else:
                    self.request.sendall(self.DataFrameFactory("failed", {}))
            if conHeader.reqtype == "getHeroesInGame":
                data = self.getHeroesInGame(d["data"])
                if len(data) > 0:
                    self.request.sendall(DataFrame(Header(0, "success"), data).toString())
                else:
                    self.request.sendall(DataFrame(Header(0, "failed")).toString())
            if conHeader.reqtype == "sendParty":
                data = self.sendParty(d["data"])
                if data == 1:
                    self.request.sendall(self.DataFrameFactory("success", {}))
                else:
                    self.request.sendall(self.DataFrameFactory("failed", {}))
            if conHeader.reqtype == "getCurrentHeroTurn":
                data = self.getCurrentHeroTurn(d["data"])
                if data != None:
                    self.request.sendall(self.DataFrameFactory("success", {"heroID" : data}))
                else:
                    self.request.sendall(self.DataFrameFactory("failed", {}))
            if conHeader.reqtype == "getHeroesInOrder":
                data = self.getHeroesInOrder(d["data"])
                if data != None:
                    self.request.sendall(self.DataFrameFactory("success", {"heroes" : data}))
                else:
                    self.request.sendall(self.DataFrameFactory("failed", {}))
        except ValueError:
            pass
    def getCurrentHeroTurn(self, data):
        gameID = data["gameID"]
        payload = "select currenthero from currentgames where id = {};".format(gameID)
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        for heroID in c:
            print "HERO ID: {}".format(heroID)
            return heroID[0]
    def sendParty(self, data):
        gameID = data["gameID"]
        playerID = data["playerID"]
        heroes = data["heroes"]
        for x in heroes:
            payload = "insert into heroesingames (GameID, heroID) values ({}, {});".format(int(gameID), int(x))
            self.sendSQLPost(payload)
        return 1
    def nextTurn(self, data):
        g = data["gameID"]
        payload = "select currenthero, nexthero from currentgames where id={};".format(int(g))
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        n = None
        for currenthero, nexthero in c:
            n = nexthero
        heroes = self.determineHeroOrder(g)
        nex = None
        for x in range(len(heroes)):
            if heroes[x].getID() == int(n):
                nex = heroes[x + 1].getID()
        payload = "update currentgames set currenthero = {}, nexthero = {} where gameID = {};".format(n, nex, int(g))
        self.sendSQLPost(payload)
        return {"gameID" : g, "hero" : n}
    def askForBoard(self, data):
        g = data["gameID"]
        payload = "select hexColumn, hexRow, heroID from currentgametiles where GameID = {};".format(str(g))
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        tiles = []
        for hexColumn, hexRow, heroID in c:
            tiles.append((hexColumn, hexRow, heroID))
        return {"tiles" : str(tiles)}
    def getHeroesInOrder(self, data):
        gameID = data["gameID"]
        heroes = self.determineHeroOrder(gameID)
        ret = []
        for x in heroes:
            ret.append(x.getJSON())
        return ret
    def getHeroesInGame(self, data):
        gameID = data["gameID"]
        print "Got hero request for gameID: {}".format(gameID)
        payload = "select heroID from heroesingames where GameID = "+str(gameID)+";"
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        heroes = []
        for heroID in c:
            print "SQL Request for heroID: {}".format(heroID[0])
            payload = "select * from heroes where heroID = {};".format(heroID[0])
            cnx2 = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
            c2 = cnx2.cursor()
            c2.execute(payload)
            h = self.makeHeroes(c2)
            for he in h:
                heroes.append(he.getJSON())
            c2.close()
            cnx2.close()
        print "Heroes: {}".format(heroes)
        return {"heroes" : heroes}
    def sendTileChoice(self, data):
        playerID = data["id"]
        row = data["row"]
        col = data["col"]
        heroID = str(data["hero"])
        gameID = data["gameID"]
        payload = "update currentgametiles set heroID="+heroID+" where hexColumn="+str(col)+" and hexRow=" +str(col)+" and GameID=" +str(gameID)+ ";"
        self.sendSQLPost(payload)
        return 1
    def determineHeroOrder(self, gameID):
        heroes = self.getHeroesInGame({"gameID" : gameID})["heroes"]
        actualHeroes = []
        for x in heroes:
            h = hero.createFromJSON(ast.literal_eval(x))
            actualHeroes.append(h)
        return sorted(actualHeroes, key=lambda her: her.getInitiative())
    def connectToGame(self, data):
        playerID = data["playerID"]
        gameID = data["gameID"]
        print "Player ID Connect To Game: {}".format(playerID)
        heroes = self.determineHeroOrder(gameID)
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        payload = "update currentgames set currenthero={},nexthero={} where id={};".format(heroes[0].getID(), heroes[1].getID(), gameID)
        c.execute(payload)
        cnx.commit()
        return 1
    def testConnectToGame(self, data):
        playerID = data["playerID"]
        print "Player ID Connect To Game: {}".format(playerID)
        payload = "select id, player2 from currentgames where player1 = {};".format(int(playerID))
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        playerid = 0
        g = None
        for gameID, ide in c:
            playerid = ide
            g = gameID
        ide, jsons = self.getHeroes({"playerID" : playerid})
        heroes = self.determineHeroOrder(g)
        payload = "update currentgames set currenthero={},nexthero={} where id={};".format(heroes[0].getID(), heroes[1].getID(), g)
        c.execute(payload)
        cnx.commit()
        return g, playerid, jsons
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
        payloadHeader = "insert into heroes ("
        payloadData = ") values ("
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
        cnx = mysql.connector.connect(user = "myuser", password = "mypass", host = "localhost", port = "8080", database="teleria")
        c = cnx.cursor()
        c.execute(payload)
        cnx.commit()
        payload = "select heroID from heroes where playerID = " + str(playerid) + ";"
        c.execute(payload)
        currhero = 0
        for heroID in c:
            if int(heroID[0]) > currhero:
                currhero = heroID[0]
        return currhero
    def checkChallenge(self, data):
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
