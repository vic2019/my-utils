#### A hash table (aka dictionary) re-implemented as an exercise ####


ARRAY_LENGTH = 419 # The index range of the hash table
SALT = 123 # A value used for the hash function. Could be any integer.


# Node object in a linked list. Each index in the hash table may point to
# a linked list consisting of these node objects.
class Node:
    def __init__(self, key, value, next_node = None):
        self.key = key
        self.value = value
        self.next_node = next_node


class Hashtable:
    def __init__(self, pairs = []):
        # Initialize the hash table
        self.__table = [None] * ARRAY_LENGTH
     
        # Add key-value pairs
        j = 0
        while j < len(pairs):
            self.update(pairs[j], pairs[j + 1])
            j += 2

        self.__reset_deleted()  
        
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
        deleted = self.__deleted # Save the deleted node for later
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
    # int of a fixed size.        
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

    # Item that has just been deleted will be saved temporarily
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

tab.clear()
assert tab.items() == []

temp = ARRAY_LENGTH
ARRAY_LENGTH = 1 # Force a hash collision (i.e. different keys produce the same index)
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

tab.clear()
assert tab.items() == []

ARRAY_LENGTH = temp
print('(Tests passed)')

