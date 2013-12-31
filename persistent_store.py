import copy
# import json
# import requests
import redis


class RedisStore:
    def store_coordinate(self, list_of_coordinates):
        r_server = redis.Redis("localhost")
        for coordinate in list_of_coordinates:
            r_server.sadd("coordinates", ','.join([str(each) for each in coordinate]))

    def store_centers(self, list_of_centers):
        r_server = redis.Redis("localhost")
        for center in list_of_centers:
            r_server.sadd("centers", ','.join([str(each) for each in center]))

    def store_address(self, coordinate, address):
        r_server = redis.Redis("localhost")
        r_server.sadd("addresses", address)

    def get_coordinate(self):
        r_server = redis.Redis("localhost")
        return r_server.spop("coordinates")

    def get_center(self):
        r_server = redis.Redis("localhost")
        return r_server.spop("centers")


# class ErrorResponse:
#     def __init__(self, message):
#         self.message = message

#     def json(self):
#         return {'message': self.message}


# class CouchDBStore:
#     """
#     Uses RESTFul APIs to connect with CouchDB
#     """
#     url = None
#     headers = {}


#     def __init__(self, host="localhost", port="5984", 
#                  headers={"Content-type": "application/json"}):
#         self.host = host
#         self.port = port
#         self.url = "http://{}:{}".format(self.host, self.port)
#         self.headers = headers


#     def get_id(self, parameter=None):
#         # We fetch a UUID from CouchDB server
#         response = requests.get("{}/_uuids/".format(self.url)).json()
#         return response["uuids"][0]


#     def put(self, db_name, data, document_id=None):
#         try:
#             # We use the uuid as id and make a new document in the db
#             if isinstance(data, dict):
#                 if not document_id:
#                     data["_id"] = self.get_id()
#                     response = requests.post("{}/{}/".format(self.url, db_name),
#                         data=json.dumps(data), headers=self.headers)
#                 else:
#                     data["_id"] = document_id
#                     response = requests.put("{}/{}/{}".format(self.url, db_name,
#                         document_id), data=json.dumps(data), headers=self.headers)
#                 return response
#             return ErrorResponse("Data provided is not a dict")
#         except Exception as e:
#             raise
#             # TODO: Change this to catch specific exceptions
#             return ErrorResponse("{} raised at put()".format(e))


#     def get(self, db_name, coordinate=None, document_id=None):
#         try:
#             if document_id:
#                 response = requests.get("{}/{}/{}".format(self.url, db_name,
#                     document_id))
#             elif coordinate:
#                 raise NotImplementedError
#             else:
#                 response = requests.get("{}/{}/_all_docs".format(self.url,
#                     db_name))
#             return response
#         except Exception as e:
#             raise
#             # TODO: Change this to catch specific exceptions
#             return ErrorResponse("{} raised at get()".format(e))


#     def document_count(self, db_name):
#         response = requests.get("{}/{}/".format(self.url, db_name))
#         return response.json()["doc_count"]


#     def get_n(self, db_name, n, processed=False):
#         if processed:
#             response = requests.get("{}/{}/_all_docs&limit={}".format(self.url,
#                 db_name, n))
#         else:
#             response = requests.get("{}/{}/_design/retrieve/_view/unprocessed?limit={}"
#                 .format(self.url, db_name, n))
#         return response


#     def delete(self, db_name, document_id):
#         document = self.get(db_name, document_id=document_id).json()
#         rev = document['_rev']
#         return requests.delete("{}/{}/{}?rev={}".format(self.url, db_name, document_id,
#             rev)).json()


# class PersistentStore(CouchDBStore):
#     """
#     TODO: Fill the docstring
#     """
#     def store(self, db_name, list_of_data, document_id=None):
#         """
#         Format is { "coordinate": ["14.562323", "75.232754"],
#                     "address": "407, Building 2, Gera Gardens, Pune" }
#         """

#         for data in list_of_data:
#             try:
#                 response = self.put(db_name=db_name, data=data,
#                     document_id=document_id)
#                 self.put(db_name="coordinates", data={"_id": response.json()["id"],
#                         "coordinate": data["coordinate"], "calculated": "false"})
#             except Exception as e:
#                 raise
#                 # TODO: Change this to catch specific exceptions
#                 return ErrorResponse("{} raised at store()".format(e))
#         return response


#     def update(self, db_name, document_id, data):
#         try:
#             document = self.retrieve(db_name=db_name, document_id=document_id)
#             for key in data:
#                 document[key] = data[key]
#             self.put(db_name=db_name, data=document)
#         except Exception as e:
#             raise
#             return {"ok": "false", "message": "{} raised at update()".format(e)}


#     def retrieve(self, db_name, coordinate=None, document_id=None, n=10,
#         processed=None):
#         if document_id:
#             response = self.get(db_name=db_name, document_id=document_id)
#         elif coordinate:
#             response = self.get(db_name=db_name, coordinate=coordinate)
#         elif processed is not None:
#             response = self.get_n(db_name=db_name, n=n, processed=processed)
#         else:
#             response = self.get(db_name=db_name)
#             # TODO: Change this to catch specific exceptions  
#         return response.json()


#     def retrieve_for_processing(self, db_name, n=10):
#         document = self.retrieve(db_name=db_name, n=n, processed=False)
#         for document in document["rows"]:
#             self.update(db_name=db_name, document_id=document["id"],
#                 data={"address": "processing"})
#         return document["rows"]


#     def count(self, db_name):
#         """
#         Returns the number of documents in the specified database
#         """
#         return self.document_count(db_name)


#     def remove(self, db_name, document_id):
#         return self.delete(db_name, document_id)


def save_to_file(address_data):
    final = {}
    keys = ["street_number", "route", "neighborhood", "sublocality",
    "administrative_area_level_2", "administrative_area_level_1", "country",
    "postal_code"]
    address_data = address_data[::-1]
    keys_reversed = copy.copy(keys)
    with open('log.log', 'a') as f:
        f.write(str(address_data)  + '\n')

    for component in address_data:
        try:
            if component['types'][0] not in keys:
                print "#", component['types'][0], "#"
                final[keys_reversed.pop()] = component['long_name']
            else:
                final[component['types'][0]] = component['long_name']
                keys_reversed.pop()
        except IndexError:
            print component['types']

    result = ''
    for key in keys:
        try:
            result += final[key]+','
        except KeyError:
            result += ','
    return result