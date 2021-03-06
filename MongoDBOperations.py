import pymongo
import pandas as pd
import json


class MongoDB_Operation_Management:


    def __init__(self, username, password):    # this function will set the required url
        try:
            self.username = username
            self.password = password
            self.url = "{}:{}--mongodb---url----".format(self.username, self.password)
        except Exception as e :
            raise Exception(f"(__init__): Something went wrong on initialization process "+str(e))

    def getMongoDBClientObject(self): # this function creates the client object for connection purpose
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client
        except Exception as e:
            raise Exception("(getMongoDBClientObject): Something went wrong on creation of client object "+str(e))

    def closeMongoDBconnection(self, mongo_client):
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception("(closeMongoDBconnection): Something went wrong while closing the connection "+str(e))

    def isDatabasePresent(self, db_name):
        try:
            mongo_client = self.getMongoDBClientObject()
            if db_name in mongo_client.list_database_names():
                mongo_client.close()
                return True
            else:
                mongo_client.close()
                return False        
        except Exception as e:
            raise Exception("(isDatabasePresent): Failed on checking if the database is present or not "+str(e))

    def createDatabase(self, db_name):
        try:
            database_status_check = self.isDatabasePresent(db_name=db_name)                        
            if not database_status_check:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
            else:
                mongo_client = self.getMongoDBClientObject()
                database = mongo_client[db_name]
                mongo_client.close()
                return database
        except Exception as e:
            raise Exception(f"(createDatabase): Failed on creating database "+str(e))      

    def getDatabase(self, db_name):
        try:
            mongo_client = self.getMongoDBClientObject()
            mongo_client.close()
            return mongo_client[db_name]
        except Exception as e:
            raise Exception(f"(getDatabase): Failed to get the database list")

    def getCollection(self, collection_name, db_name):
        try:
            database = self.getDatabase(db_name) 
            return database[collection_name]
        except Exception as e:
            raise Exception(f"(getCollection): Failed to get the database list.")

    def isCollectionPresent(self, collection_name, db_name):
        try:
            database_status_check = self.isDatabasePresent(db_name)
            if database_status_check:
                database = self.getDatabase(db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"(isCollectionPresent): Failed to check collection\n" + str(e)) 

    def createCollection(self, collection_name, db_name):
        try:
            collection_status_check = self.isCollectionPresent(collection_name, db_name)                           
            if not collection_status_check:
                database = self.getDatabase(db_name= db_name)
                collection = database[collection_name]
                return collection
        except Exception as e:
            raise Exception(f"(createCollection): Failed to create collection {collection_name}\n" + str(e))

    def dropCollection(self, collection_name, db_name):
        try:
            collection_check_status = self.isCollectionPresent(collection_name, db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name, db_name)
                collection.drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(dropCollection): Failed to drop collection {collection_name}")

    def insertRecord(self, collection_name, db_name, records):
        try:
            collection = self.getCollection(collection_name, db_name)
            record  = list(records.values())
            collection.insert_many(record)
            sum = 0
            return f"row insert"
        except Exception as e:
            raise Exception(f"(insertRecords): Something went wrong on inserting record\n" + str(e))

    def findfirstrecord(self, db_name, collection_name, query=None):
        try:
            collection_check_status = self.isCollectionPresent(collection_name, db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name, db_name)
                firstrecord = collection.find_one(query)
                return firstrecord
        except Exception as e:
            raise Exception(f"(findRecord): Failed to find record for the given collection and database\n" + str(e))

    def findAllRecords(self, db_name, collection_name):
        try:
            collection_check_status = self.isCollectionPresent(collection_name, db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name, db_name)
                findallrecords = collection.find()
                return findallrecords
        except Exception as e:
            raise Exception(f"(findAllRecords): Failed to find record for the given collection and database\n" + str(e))                                                                        

    def findRecordOnQuery(self, db_name, collection_name, query):
        try:
            collection_check_status = self.isCollectionPresent(collection_name, db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name, db_name)
                findRecords = collection.find(query)
                return findRecords
        except Exception as e:
            raise Exception(f"(findRecordOnQuery): Failed to find record for given query,collection or database\n" + str(e))

    def updateOneRecord(self, collection_name, db_name, query):
        try:
            collection_status = self.isCollectionPresent(collection_name, db_name)
            if collection_status:
                collection = self.getCollection(collection_name=collection_name, db_name=db_name)
                previous_record = self.findAllRecords(db_name=db_name, collection_name=collection_name)
                new_record = query
                update_record = collection.update_one(previous_record, new_record)
                return update_record
        except Exception as e:
            raise Exception(f"(updateRecord): Failed to update the records with given collection query or database name.\n" + str(e))

    def deleteRecord(self, db_name, collection_name, query):
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, db_name=db_name)
                collection.delete_one(query)
                return "1 row deleted"
        except Exception as e:
            raise Exception(
                f"(deleteRecord): Failed to update the records with given collection query or database name.\n" + str(e))

    def deleteRecords(self, db_name, collection_name, query):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            if collection_check_status:
                collection = self.getCollection(collection_name=collection_name, db_name=db_name)
                collection.delete_many(query)
                return "Multiple rows deleted"
        except Exception as e:
            raise Exception(
                f"(deleteRecords): Failed to update the records with given collection query or database name.\n" + str(
                    e))

    def getDataFrameOfCollection(self, db_name, collection_name):
        """
        """
        try:
            all_Records = self.findAllRecords(collection_name=collection_name, db_name=db_name)
            dataframe = pd.DataFrame(all_Records)
            return dataframe
        except Exception as e:
            raise Exception(
                f"(getDataFrameOfCollection): Failed to get DatFrame from provided collection and database.\n" + str(e))

    def saveDataFrameIntoCollection(self, collection_name, db_name, dataframe):
        """
        """
        try:
            collection_check_status = self.isCollectionPresent(collection_name=collection_name, db_name=db_name)
            dataframe_dict = json.loads(dataframe.T.to_json())
            if collection_check_status:
                self.insertRecords(collection_name=collection_name, db_name=db_name, records=dataframe_dict)
                return "Inserted"
            else:
                self.createDatabase(db_name=db_name)
                self.createCollection(collection_name=collection_name, db_name=db_name)
                self.insertRecords(db_name=db_name, collection_name=collection_name, records=dataframe_dict)
                return "Inserted"
        except Exception as e:
            raise Exception(
                f"(saveDataFrameIntoCollection): Failed to save dataframe value into collection.\n" + str(e))

    def getResultToDisplayOnBrowser(self, db_name, collection_name):
        """
        This function returns the final result to display on browser.
        """
        try:
            response = self.findAllRecords(db_name=db_name, collection_name=collection_name)
            result = [i for i in response]
            return result
        except Exception as e:
            raise Exception(
                f"(getResultToDisplayOnBrowser) - Something went wrong on getting result from database.\n" + str(e))                        
        