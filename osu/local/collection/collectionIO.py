import math
import lzma, struct, datetime

from osu.local.hitobject.std.std import Std
from osu.local.hitobject.mania.mania import Mania


class CollectionIO():

    def __init__(self, data):
        self.offset = 0
        self.version = None
        self.num_collections = None

        self.collections = {}

        self.__parse_version(data)
        for _ in range(self.num_collections):
            self.__add_entry(*self.__parse_collection(data))

    
    def __add_entry(self, name, md5_map_hashes):
        self.collections[name] = md5_map_hashes


    def __parse_version(self, data):
        format_specifier = '<ii'
        self.version, self.num_collections = struct.unpack_from(format_specifier, data, self.offset)
        self.offset += struct.calcsize(format_specifier)


    def __parse_collection(self, data):
        name = self.__parse_string(data)
        num_maps = struct.unpack_from('i', data, self.offset)[0]
        self.offset += struct.calcsize('i')
        
        md5_map_hashes = []
        for _ in range(num_maps):
            md5_map_hashes.append(self.__parse_string(data))

        return name, md5_map_hashes


    def __parse_string(self, data):
        if data[self.offset] == 0x00:
            begin = self.offset = self.offset + 1

            while data[self.offset] != 0x00: 
                self.offset += 1
            
            self.offset += 1
            return data[begin : self.offset - 2].decode('utf-8')
        
        elif data[self.offset] == 0x0b:
            self.offset += 1
            
            string_length = self.__decode(data)
            offset_end    = self.offset + string_length
            string = data[self.offset : offset_end].decode('utf-8')
            
            self.offset = offset_end
            return string

        else:
            #TODO: Replace with custom exception
            raise Exception(f'Invalid data\noffset: {self.offset}\nData: {data[self.offset]}')


    def __decode(self, binarystream):
        result = 0
        shift = 0

        while True:
            byte = binarystream[self.offset]
            self.offset += 1
            result = result |((byte & 0b01111111) << shift)
            if (byte & 0b10000000) == 0x00: break
            shift += 7

        return result


    @staticmethod
    def open_collection(collection_path):
        with open(collection_path, 'rb') as f:
            data = f.read()
        return CollectionIO(data)