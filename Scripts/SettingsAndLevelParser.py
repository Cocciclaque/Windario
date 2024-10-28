class Config:

    def __init__(self, configFileName:str, aliasFileName:str):
        self.config:dict = self.parseConfig(configFileName)
        self.alias:dict = self.parseElementAlias(aliasFileName)

    def parseConfig(self, configFileName):
        f = open((configFileName), "r")
    
        params:dict = {}

        for line in f.readlines():
            if line != "":
                params[line.rsplit()[0].split(":")[0]] = line.rsplit()[0].split(":")[1]

        return params
    
    def parseElementAlias(self, aliasFileName):
        f = open((aliasFileName), "r")

        alias = {}

        for line in f.readlines():
            if line != "":
                alias[line.rsplit()[0].split("=")[0]] = line.rsplit()[0].split("=")[1]
        
        return alias

class Level:

    def __init__(self, levelFileName:str):
        self.map:str = self.parseLevel(levelFileName)

    def parseLevel(self, levelFileName):
        f = open((levelFileName), "r")

        mapTemp = []

        for line in f.readlines():
            mapTemp.append(line.rsplit()[0])

        return mapTemp
