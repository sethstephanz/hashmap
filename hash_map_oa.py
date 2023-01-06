# Description: This file contains several methods for manipulating data within a HashMap that uses open addressing
# and quadratic probing to avoid collisions.


from a6_include import (DynamicArray, DynamicArrayException, HashEntry, hash_function_1, hash_function_2)

class HashMap:

    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
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
        This method adds a value into a hash table and, if the indexed spot is full, probes until an empty spot is found.
        If the key is already in the array, replace
        """
        # Quadratic probing: i = (initial + j2) % m(where, j=1, 2, 3, …)

        table_load = self.table_load()
        hashed_key = self._hash_function(key)
        new_hash_entry = HashEntry(key, value)

        if table_load >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        # j ** 0 assesses to 0, so start j at 0 instead of 1

        j = 0
        ts_found = False
        ts_index = 0

        while True:
            index = (hashed_key + j ** 2) % self.get_capacity()
            # if the bucket's empty, add the item
            if not self._buckets[index]:
                if ts_found:
                    index = ts_index
                self._buckets.set_at_index(index, new_hash_entry)
                self._size += 1
                return
            # test for if it's a tombstone
            elif self._buckets[index].is_tombstone and not ts_found:
                ts_found = True
                ts_index = index
            elif self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            j += 1

    def table_load(self) -> float:
        """
        This method calculates table load and returns that figure
        """
        size = self.get_size()
        capacity = self.get_capacity()
        table_load = size / capacity
        return table_load

    def empty_buckets(self) -> int:
        """
        This method returns how many empty buckets there are in a given hash table
        """
        index = 0
        counter = 0
        while index < self._buckets.length():
            if not self._buckets[index] or self._buckets[index].is_tombstone:
                counter += 1
            index += 1
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        This method is used to resize an existing hash table
        """
        # catch for invalid capacities
        # this should always be the case? keep just in case
        if new_capacity < 1 or new_capacity < self.get_size():
            return

        # else, see if the new capacity is prime. if it isn't, find next prime and set that to new capacity
        if new_capacity > 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        # save old values
        old_table = self._buckets

        # declare self._buckets to be empty dynamic array
        # override old self._buckets and create new dynamic array with open slots
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for _ in range(self._capacity):
            self._buckets.append(None)  # this might be causing problems with the iter/next?
        self._size = 0  # to prevent looping

        index = 0
        while index < old_table.length():
            if old_table[index]:  # if has a value
                if not old_table[index].is_tombstone:  # and if it's not a tombstone
                    key = old_table[index].key
                    value = old_table[index].value
                    self.put(key, value)
            index += 1

    def get(self, key: str) -> object:
        """
        This method is called to retrieve a value if the input key is present in the table. Else, return none
        """

        hashed_key = self._hash_function(key)

        j = 0
        while True:
            index = (hashed_key + j ** 2) % self.get_capacity()
            if not self._buckets[index]:
                return None
            elif self._buckets[index].key == key:
                if self._buckets[index].is_tombstone:
                    return None
                else:
                    return self._buckets[index].value
            j += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method searches the dynamic array and returns True if the key is found; returns False if not.
        """
        hashed_key = self._hash_function(key)
        j = 0
        while True:
            index = (hashed_key + j ** 2) % self.get_capacity()
            if not self._buckets[index]:
                return False
            elif self._buckets[index].key == key:
                return True
            j += 1

    def remove(self, key: str) -> None:
        """
        This method searches the array and removes an item if the input key is found. If it isn't present, this
        method does nothing
        """
        hashed_key = self._hash_function(key)
        j = 0
        while True:
            index = (hashed_key + j ** 2) % self.get_capacity()
            if not self._buckets[index]:
                return
            elif self._buckets[index].key == key:
                if not self._buckets[index].is_tombstone:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                return
            j += 1

    def clear(self) -> None:
        """
        This method clears the contents of a hashmap without resetting its capacity
        """
        index = 0
        while index < self.get_capacity():
            self._buckets[index] = None
            index += 1
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method searches an array and returns a new dynamic array that contains
        each key/value pair (formatted as tuples)
        """
        new_array = DynamicArray()

        index = 0
        while index < self._buckets.length():
            # don't want to append a bunch of 'None's to the list, so check if exists first
            if self._buckets[index]:
                if not self._buckets[index].is_tombstone:
                    key = self._buckets[index].key
                    value = self._buckets[index].value
                    new_array.append((key, value))
            index += 1
        return new_array

    def __iter__(self):
        """
        This method allows a HashTable to iterate across itself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone:
                self._index += 1
        except DynamicArrayException:
            raise StopIteration

        try:
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value
