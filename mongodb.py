import json
from pymongo import MongoClient

#Connecting with database
client = MongoClient('localhost',27017)

#Databse listing
# print(client.list_database_names())

#Collections listing
db=client.chatbot
# print(db.list_collection_names())

#Counting number of documents
# print(db.admission.count_documents({}))

#To see the data
String=""
cursor = db.admission.find({})
for i in cursor:
    del i['_id']
    result = json.dumps(i)
    String+=result+",\n\n"
# print(String)


#saving data in a jason file for later use
text_file = open("intents.json", "w")
n = text_file.write("""{\n"intents": [\n"""+String+"""{"tag": "", "patterns": [""], "responses": [""]}"""+"\n]}")
text_file.close()
print("Database imported Successfully!!")



