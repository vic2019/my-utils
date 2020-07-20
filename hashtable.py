#### A hash table (aka dictionary) re-implemented as an exercise ####


TABLE_LENGTH = 97 # The starting index range of the hash table
SALT = 123 # A value used for the hash function. Could be any integer.
LENGTH_RATIO = 1.3


# Node object in a linked list. Each index in the hash table may point to
# a linked list consisting of these node objects.
class Node:
    def __init__(self, key, value, next_node = None):
        self.key = key
        self.value = value
        self.next_node = next_node


class Hashtable:
    def __init__(self, pairs = [], table_length = TABLE_LENGTH):
        self.__table_length = table_length
        self.__salt = SALT
        self.__length_ratio = LENGTH_RATIO
        self.__len = 0
        self.__reset_deleted()

        # Initialize the hash table
        self.__table, self.__table_length = \
            self.__create_table(pairs, self.__table_length)
        
    def get(self, key):
        index = self.__hash(key, self.__table_length)
        result_node = self.__lookup(self.__table[index], key)
        return None if not result_node else result_node.value

    def update(self, key, value):
        if int(self.__len * self.__length_ratio) > self.__table_length:
            new_table_length = self.__table_length * 2 + 1
            pairs = self.items()
            self.__table, self.__table_length = \
                self.__create_table(pairs, new_table_length)
                    
        index = self.__hash(key, self.__table_length)
        self.__table[index] = self.__append(self.__table[index], key, value)
        return (key, value)

    def delete(self, key):
        index = self.__hash(key, self.__table_length)
        self.__table[index] = self.__delete(self.__table[index], key)
        deleted = self.__deleted # Save the deleted node for later
        self.__reset_deleted()
        return None if not deleted else (deleted.key, deleted.value)

    def items(self):
        output = []
        for i in range(self.__table_length):
            self.__items(self.__table[i], output)
        return output

    def keys(self):
        output = []
        for i in range(self.__table_length):
            self.__keys(self.__table[i], output)
        return output

    def clear(self):
        self.__init__()

    def copy(self):
        output = Hashtable()
        for key, value in self.items():
            output.update(key, value)
        return output
        
    def table_length(self):
        return self.__table_length

    # A hash function is a function that converts a string of any size to an
    # int of a fixed size.        
    def __hash(self, key, table_length):
        key = str(key)
        hash_value = 0
        for char in key:
            hash_value = ord(char) + self.__salt * hash_value
        return abs(hash_value % table_length)

    def __create_table(self, pairs, table_length):
        # self.__append() has the side effect of incrementing self.__len.
        # Reset __len for the new table
        self.__len = 0
        table = [None] * table_length

        # Add key-value pairs
        if len(pairs) and type(pairs[0]) is tuple: # Or isinstance(pairs[0], tuple)
            for key, value in pairs:
                index = self.__hash(key, table_length)
                table[index] = self.__append(table[index], key, value)

        else: # Use alternative input format if applicable
            j = 0
            while j < len(pairs):
                key, value = pairs[j], pairs[j + 1]
                index = self.__hash(key, table_length)
                table[index] = self.__append(table[index], key, value)
                j += 2

        return (table, table_length)

    def __lookup(self, node, key):
        if node == None:
            return None
        elif node.key == key:
            return node
        else:
            return self.__lookup(node.next_node, key)

    def __append(self, node, key, value):
        if node == None:
            self.__len += 1
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
            self.__len-= 1
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
        return self.__len

    def __repr__(self):
        return "<class 'hashtable'> " + '{'+ str(self.items())[1:-1] + '}'



# Tests
tab = Hashtable(['CA', 'Sacramento', 'TX', 'Austin', 'NY', 'NYC'])
assert len(tab.keys()) == 3
assert len(tab.items()) == 3
assert len(tab) == 3
assert tab.get('CA') == 'Sacramento'
assert tab.get('TX') == 'Austin'
assert tab.get('FL') == None
assert tab.delete('TX') == ('TX', 'Austin')
assert tab.get('TX') == None
assert len(tab.keys()) == 2
assert tab.get('CA') == 'Sacramento'
assert tab.delete('FL') == None
assert len(tab) == 2
assert tab.update('CA', 'Sac.') == ('CA', 'Sac.')
assert tab.get('CA') == 'Sac.'

tab2 = tab.copy()
tab.update('NY', 'Big Apple')
assert tab.get('NY') == 'Big Apple'
assert tab2.get('NY') == 'NYC'
tab3 = Hashtable([(1, 1.3), ('Two', 2), (3.5, ['a', 'b', 'c'])])
assert len(tab3) == 3
assert tab3.get('Two') == 2
assert tab3.get(3.5).pop() == 'c'
tab.clear()
tab2.clear()
tab3.clear()
assert tab.items() == []

temp = TABLE_LENGTH
TABLE_LENGTH = 1
tab = Hashtable(['CA', 'Sacramento', 'TX', 'Austin', 'NY', 'NYC'])
assert len(tab.keys()) == 3
assert len(tab.items()) == 3
assert len(tab) == 3
assert tab.get('CA') == 'Sacramento'
assert tab.get('TX') == 'Austin'
assert tab.get('FL') == None
assert tab.delete('TX') == ('TX', 'Austin')
assert tab.get('TX') == None
assert len(tab.keys()) == 2
assert tab.get('CA') == 'Sacramento'
assert tab.delete('FL') == None
assert len(tab) == 2
assert tab.update('CA', 'Sac.') == ('CA', 'Sac.')
assert tab.get('CA') == 'Sac.'

tab2 = tab.copy()
tab.update('NY', 'Big Apple')
assert tab.get('NY') == 'Big Apple'
assert tab2.get('NY') == 'NYC'
tab3 = Hashtable([(1, 1.3), ('Two', 2), (3.5, ['a', 'b', 'c'])])
assert len(tab3) == 3
assert tab3.get('Two') == 2
assert tab3.get(3.5).pop() == 'c'

# Set initial table length to 1
tab4 = Hashtable([('???', None), ('empty', []), (3.14, 'Pi')], 1)
assert tab4.table_length() <= 7
assert len(tab4) == 3
assert len(tab4.items()) == 3
for i in range(0, 100):
    tab4.update(i, i)
assert len(tab4) == 103
assert tab4.get(99) == 99
assert tab4.table_length() > 103
tab.clear()
tab2.clear()
tab3.clear()
tab4.clear()
assert tab4.items() == []

TABLE_LENGTH = temp
print('[Tests passed]')
