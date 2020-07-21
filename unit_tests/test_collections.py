import unittest

from osu.local.collection.collectionIO import CollectionIO


class TestCollections(unittest.TestCase):

    @staticmethod
    def test_collection_loading(filepath):
        collection = CollectionIO.open_collection(filepath)

        endl = '\n'
        print(f'Collections: {endl.join(list(collection.collections.keys()))}')