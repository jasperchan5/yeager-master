import pymongo

class SolitaireDB:
    def __init__(self,input):
        self.__char = input
        self.__client = pymongo.MongoClient("mongodb+srv://jasperchan:jscnn51011@cluster0.p9bjf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def setSequence(self,category,input):
        soli_db = self.__client['Solitaire']
        collection = soli_db[category]
        if category != 'nowSequence':
            processedInput = [input[i:i+1] for i in range(0, len(input), 1)]
            for i in range(len(processedInput)):
                collection.insert_one({
                    "content": processedInput[i],
                    "number": i
                })
        else:
            collection.insert_one({
                "sequence": input,
                "number":0
                })
    # Set the sequence being said now
    def setNow(self):
        soli_db = self.__client['Solitaire']
        allCollection = soli_db.list_collection_names()
        for i in range(len(allCollection)):
            if allCollection[i] != 'nowSequence':
                tempCollection = soli_db[allCollection[i]]
                if tempCollection.find_one({'content':self.__char,'number':0}):
                    # print("found ",self.__char," in collection ",allCollection[i])
                    self.clearSequence("nowSequence")
                    self.setSequence("nowSequence",allCollection[i])

    def querySequence(self):
        self.setNow()
        soli_db = self.__client['Solitaire']
        currentSequence = soli_db['nowSequence'].find_one({"number":0})['sequence']
        collection = soli_db[currentSequence]
        matchChar = collection.find_one({"content": self.__char})
        return str(collection.find({})[matchChar["number"]+1]["content"])

    def clearSequence(self,category):
        soli_db = self.__client['Solitaire']
        collection = soli_db[category]
        collection.delete_many({})
    
    def printCollection(self):
        soli_db = self.__client['Solitaire']
        print(soli_db.list_collection_names())


# soliModel = SolitaireDB(input())
# print(soliModel.querySequence())
