# Laron Lemon, Student ID: #000927228


# hash table class
class HashTable:
    def __init__(self):
        self.size = 1
        self.hash_array = [None] * self.size

# creates hash
    def _get_hash(self, key):
        h = 0
        for char in str(key):
            h += ord(char)
        return h % 1

# insert into hash table
    def insert(self, key: object, value: object) -> object:
        key_hash = self._get_hash(key)
        key_value = [key, value]
        self.size += 1

        if self.hash_array[key_hash] is None:
            self.hash_array[key_hash] = list([key_value])
            return True
        else:
            for pair in self.hash_array[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.hash_array[key_hash].append(key_value)
            return True

# search hash table using key -> returns value
    def search(self, key):
        key_hash = self._get_hash(key)
        if self.hash_array[key_hash] is not None:
            for pair in self.hash_array[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

# remove item from hash table using the key
    def remove(self, key):
        key_hash = self._get_hash(key)

        if self.hash_array[key_hash] is None:
            return False
        for i in range(0, len(self.hash_array[key_hash])):
            if self.hash_array[key_hash][i][0] == key:
                self.hash_array[key_hash].pop(i)
                return True

# print the hash table
    def print(self):
        for item in self.hash_array:
            if item is not None:
                print(str(item))



