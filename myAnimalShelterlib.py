from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:53800/?authMechanism=DEFAULT&authSource=AAC' % (username, password))
        # where xxxx is your unique port number
        self.database = self.client['AAC']

    # Create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            if self.database.animals.insert_one(data):  # data should be dictionary       
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False
    
    def read_all_dogs(self,data):
        # Query the collection for all documents whose breed is "dog"
        cursor = self.database.animals.find({"animal_type": "Dog"})

        # Return the cursor
        return cursor
    
    def read_all(self,data):
        cursor = self.database.animals.find(data)
        return cursor
        
        
    # Create method to implement the R in CRUD.
    def read(self, query):
        # If query is None, return all documents in the collection
        if query is not None:
            return self.database.animals.find(query)
        # Otherwise, query the collection for matching documents
        else:
            raise Exception("Nothing to search, the query is empty")
            
    def update(filter_dict, update_dict):
        try:
            # Update the documents that match the filter
            result = self.database.animals.update_many(filter_dict, {"$set": update_dict})

            # Return the result as JSON
            return {"updated_count": result.modified_count}
        except Exception as e:
            # Return the MongoDB error message
            return {"error": str(e)}
        
    def delete(filter_dict):
        try:
            # Delete the documents that match the filter
            result = self.database.animals.delete_many(filter_dict)

            # Return the result as JSON
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            # Return the MongoDB error message
            return {"error": str(e)}
    
    def get_dog_breeds(self):
        return self.database.animals.distinct('breed', {'animal_type': 'Dog'})