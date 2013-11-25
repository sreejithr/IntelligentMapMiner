import unittest

from persistent_store import PersistentStore

DB_NAME = "addresses"
SECONDARY_DB_NAME = "coordinates"

class TestPersistentStore(unittest.TestCase):
	def setUp(self):
		self.data = [{'coordinate': ['18.56988', '73.93912'], 'address': None},
					 {'coordinate': ['18.46416', '73.84365'], 'address': None},
					 {'coordinate': ['18.46421', '73.84325'], 'address': None},
					 {'coordinate': ['18.46429', '73.83855'], 'address': None},
					 {'coordinate': ['18.46437', '73.8384'], 'address': None},
					 {'coordinate': ['18.4644', '73.83821'], 'address': None},
					 {'coordinate': ['18.46452', '73.83778'], 'address': None},
					 {'coordinate': ['18.4642', '73.83793'], 'address': None},
					 {'coordinate': ['18.46413', '73.8381'], 'address': None}]

		self.single_data = [{'coordinate': ['100.56988', '100.93912'],
							 'address': None}]

		self.persistent_store = PersistentStore()

	
	def test_store(self):
		# Test the 'addresses' db
		initial_count = self.persistent_store.count(DB_NAME)
		initial_coordinate_count = self.persistent_store.count(SECONDARY_DB_NAME)

		response = self.persistent_store.store(DB_NAME, list_of_data=self.data)
		final_count = self.persistent_store.count(DB_NAME)

		self.assertTrue(response.json()['ok'])
		self.assertEqual((final_count - initial_count), 9)

		# Test the 'coordinates' db
		final_coordinate_count = self.persistent_store.count(SECONDARY_DB_NAME)
		self.assertEqual((final_coordinate_count - initial_coordinate_count), 9)


	def test_retrieve(self):
		# Test bulk retrieve
		count = self.persistent_store.count(DB_NAME)
		response = self.persistent_store.retrieve(DB_NAME)
		self.assertEqual(len(response.json()['rows']), count)

		# Test retrieve by document_id
		self.persistent_store.store(DB_NAME, list_of_data=self.single_data,
			document_id="55595afcb06b1089c831004882012197")
		response = self.persistent_store.retrieve(DB_NAME, 
			document_id="55595afcb06b1089c831004882012197")
		self.assertEqual(response.json()["coordinate"], ['100.56988','100.93912'])
		self.persistent_store.remove(DB_NAME, "55595afcb06b1089c831004882012197")


	def test_retrieve_for_processing(self):
		response = self.persistent_store.retrieve_for_processing(DB_NAME, n=3)
		print response


if __name__ == '__main__':
	unittest.main()