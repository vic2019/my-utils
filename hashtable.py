#### A hash table (aka dictionary) re-implemented as an exercise ####


ARRAY_LENGTH = 1000 # The index range of the hash table
SALT = 2021 # A value used for the hash function. Could be any number.


# Node object in a linked list. Each index in the hash table may point to
# such a linked list.
class Node:
    def __init__(self, key, value, next_node = None):
        self.key = key
        self.value = value
        self.next_node = next_node


class Hashtable:
    def __init__(self, pairs = []):
        # Initialize the hash table. This is only for illustration purpose and
        # is super inefficient because Python <list> is not fixed-length array.
        self.__table = []
        for i in range(0, ARRAY_LENGTH):
            self.__table.append(None)
            
        # Add key-value pairs
        j = 0
        while j < len(pairs):
            self.update(pairs[j], pairs[j + 1])
            j += 2

        self.__reset_deleted() # Set self.__deleted to None  
        
    def get(self, key):
        index = self.__hash(key)
        result_node = self.__lookup(self.__table[index], key)
        return None if result_node == None else result_node.value

    def update(self, key, value):
        index = self.__hash(key)
        self.__table[index] = self.__append(self.__table[index], key, value)
        return (key, value)

    def delete(self, key):
        index = self.__hash(key)
        self.__table[index] = self.__delete(self.__table[index], key)
        deleted = self.__deleted # Will return the deleted key-value pair below
        self.__reset_deleted()
        return None if deleted == None else (deleted.key, deleted.value)

    def items(self):
        output = []
        for i in range(ARRAY_LENGTH):
            self.__items(self.__table[i], output)
        return output

    def keys(self):
        output = []
        for i in range(ARRAY_LENGTH):
            self.__keys(self.__table[i], output)
        return output

    def clear(self):
        self.__init__()

    def copy(self):
        output = Hashtable()
        for key, value in self.items():
            output.update(key, value)
        return output
        

    # A hash function is a function that converts a string of any size to an
    # int of a fixed size. Here, the fixed size is 2 digit.        
    def __hash(self, key):
        key = str(key)
        hash_value = 0
        for char in key:
            hash_value = ord(char) + SALT * hash_value
        return abs(hash_value % ARRAY_LENGTH)

    def __lookup(self, node, key):
        if node == None:
            return None
        elif node.key == key:
            return node
        else:
            return self.__lookup(node.next_node, key)

    def __append(self, node, key, value):
        if node == None:
            return Node(key, value)
        elif node.key == key:
            node.value = value
            return node
        else:
            node.next_node = self.__append(node.next_node, key, value)
            return node

    def __delete(self, node, key):
        if node == None:
            return None
        elif node.key == key:
            self.__deleted = node
            return node.next_node
        else:
            node.next_node = self.__delete(node.next_node, key)
            return node

    # Item that has just been deleted will be saved here temporarily
    def __reset_deleted(self):
        self.__deleted = None

    def __items(self, node, output):
        if node == None:
            return
        output.append((node.key, node.value))
        self.__items(node.next_node, output)

    def __keys(self, node, output):
        if node == None:
            return
        output.append(node.key)
        self.__keys(node.next_node, output)

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return "<class 'hashtable'> " + '{'+ str(self.items())[1:-1] + '}'



    ### This method is a test. It simulates hash collision (when different keys
    ### return the same number). It is not part of the module's features
    def run_test(self, INDEX = 0):
        self.__table[INDEX] = self.__append(self.__table[INDEX], 'France', 'Paris')
        self.__table[INDEX] = self.__append(self.__table[INDEX], 'US', 'DC')
        self.__table[INDEX] = self.__append(self.__table[INDEX], 'China', 'Beijing')

        assert self.__lookup(self.__table[INDEX], 'France').value == 'Paris'
        assert self.__lookup(self.__table[INDEX], 'China').value == 'Beijing'
        assert self.__lookup(self.__table[INDEX], 'US').value == 'DC'

        self.__table[INDEX] = self.__delete(self.__table[INDEX], 'France')
        deleted = self.__deleted
        self.__reset_deleted()
        assert deleted.value == 'Paris'
        assert self.__lookup(self.__table[INDEX], 'France') == None
        assert self.__lookup(self.__table[INDEX], 'US').value == 'DC'
        assert self.__lookup(self.__table[INDEX], 'China').value == 'Beijing'

        self.__table[INDEX] = self.__delete(self.__table[INDEX], 'US')
        deleted = self.__deleted
        self.__reset_deleted()
        assert deleted.value == 'DC'
        assert self.__lookup(self.__table[INDEX], 'France') == None
        assert self.__lookup(self.__table[INDEX], 'US') == None
        assert self.__lookup(self.__table[INDEX], 'China').value == 'Beijing'
        
        self.__table[INDEX] = self.__delete(self.__table[INDEX], 'China')
        deleted = self.__deleted
        self.__reset_deleted()
        assert self.__lookup(self.__table[INDEX], 'France') == None
        assert self.__lookup(self.__table[INDEX], 'US') == None
        assert self.__lookup(self.__table[INDEX], 'China') == None



# Tests
tab = Hashtable(['CA', 'Sacramento', 'TX', 'Austin', 'NY', 'NYC'])
assert len(tab.keys()) == 3
assert len(tab.items()) == 3
assert len(tab) == 3
assert tab.get('CA') == 'Sacramento'
assert tab.get('TX') == 'Austin'
assert tab.delete('TX') == ('TX', 'Austin')
assert tab.get('TX') == None
assert tab.get('CA') == 'Sacramento'
tab2 = tab.copy()
tab.update('NY', 'Big Apple')
assert tab.get('NY') == 'Big Apple'
assert tab2.get('NY') == 'NYC'

assert tab.update('a', 42) == ('a', 42)
assert tab.get('a') == 42
assert tab.update('a', 'World Peace')
assert tab.get('a') == 'World Peace'
assert tab.delete('a') == ('a', 'World Peace')
assert tab.delete('a') == None
assert tab.get('a') == None

assert tab.get('b') == None
assert tab.delete('b') == None

tab.run_test(0)
tab.run_test(999)

import random
for i in range(10000):
    key = str(random.randint(0, 10000))
    value = str(random.randint(0, 10000))
    assert tab.update(key, value) == (key, value)
    assert tab.get(key) == value
    assert tab.delete(key) == (key, value)
    assert tab.get(key) == None

tab.clear()
assert tab.items() == []

print('(Tests passed)')

