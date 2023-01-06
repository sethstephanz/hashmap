# Description: This file contains several methods for manipulating data within a HashMap that uses linked lists
# to avoid collisions.


from a6_include import (DynamicArray, LinkedList, hash_function_1, hash_function_2)

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #


    def put(self, key: str, value: object) -> None:
        """
        This method adds a key:value pair to a hash table (and calls resize, if necessary).
        """
        # IF KEY IS ALREADY IN HASHMAP, REPLACE OLD VALUE WITH NEW VALUE
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hashed_key = self._hash_function(key)
        index = hashed_key % self.get_capacity()

        if not self.contains_key(key):
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            # key is already present in structure; need to override value. DON'T INCREASE SIZE
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value

    def empty_buckets(self) -> int:
        """
        This method returns how many empty buckets there are within a given hashmap
        """
        # print('empty_buckets')
        # each 'empty' node in a HashMap DA is the head of a (empty) linked list, so assess by using length
        index = 0
        counter = 0
        while index < self._buckets.length():
            if self._buckets[index].length() == 0:
                counter += 1
            index += 1
        return counter

    def table_load(self) -> float:
        """
        This method calculates and returns the current table load (amount of items divided by capacity of table)
        """
        # divide size by capacity to get table load
        table_load = self.get_size() / self.get_capacity()
        return table_load

    def clear(self) -> None:
        """
        This method is used to clear a table. It clears the individual buckets but leaves the original
        capacity intact.
        """
        index = 0
        while index < self._buckets.length():
            self._buckets[index] = LinkedList()
            index += 1
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method is used to resize an existing hash table
        """
        # catch for invalid capacities
        if new_capacity < 1:
            return

        if new_capacity >= 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        # save old values
        old_table = self._buckets

        # declare self._buckets to be empty dynamic array
        # override old self._buckets and create new dynamic array with open slots
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0 # to prevent looping

        index = 0
        while index < old_table.length():
            for node in old_table[index]:
                self.put(node.key, node.value)
            index += 1

    def get(self, key: str):
        """
        This method searches for a key and, if found, returns the value associated with that key.
        If it's not found, this method does nothing
        """

        hashed_key = self._hash_function(key)
        index = hashed_key % self.get_capacity()

        for node in self._buckets[index]:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if input key is present in hashmap. Else, it returns False
        """
        hashed_key = self._hash_function(key)
        index = hashed_key % self.get_capacity()

        for node in self._buckets[index]:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes an input key
        """
        hashed_key = self._hash_function(key)
        index = hashed_key % self.get_capacity()
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                bucket.remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of the key/value pairs contained
        in the hashmap (order doesn't matter).
        """
        new_array = DynamicArray()

        index = 0
        while index < self._buckets.length():
            for node in self._buckets[index]:
                new_tuple = (node.key, node.value)
                new_array.append(new_tuple)
            index += 1
        return new_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This standalone method receives a (not nec. sorted) dynamic array. It then returns a tuple containing
    a dynamic array containing the most commonly occurring values in the array and an integer that contains
    the amount of times that value/those values appear: (['value(s)'], frequency).
    """

    map = HashMap(da.length())
    most_common = DynamicArray()
    frequency = 0

    index = 0
    while index < da.length():
        value = map.get(da[index])
        key = da[index]
        if value:
            value += 1
        else:
            value = 1
        map.put(key, value)
        if value > frequency:
            most_common = DynamicArray()
            frequency = value
            most_common.append(key)
        elif value == frequency:
            most_common.append(key)
        index += 1
    return most_common, frequency
