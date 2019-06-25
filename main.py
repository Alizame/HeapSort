"""Sorts an array from a file and prints intermediate steps + the sorted array"""

import math
from typing import List

FILE = "data.txt"
MY_ARRAY = []

try:
    with open(FILE, 'r') as f:
        for line in f:
            MY_ARRAY.append(int(line))
except ValueError:
    print("Error in file, couldnt parse to int, exiting!")
    exit()


def _get(a: List[int], i: int, default=None):
    """Returns the number of the index of the array"""
    try:
        return a[i]
    except IndexError as _:
        return default


def heap_seepin(a: List[int], node_index: int, last_index: int = None) -> None:
    """Lets a number seep into the heap"""
    last_index = last_index if last_index is not None else len(a) - 1

    left_index = node_index * 2 + 1  # +1 because lists start at 0
    right_index = node_index * 2 + 2

    if left_index <= last_index:
        try:
            if a[node_index] > a[left_index]:  # if node bigger than left-leaf:
                a[node_index], a[left_index] = a[left_index], a[node_index]  # switch them around
                heap_seepin(a, left_index, last_index)  # re-evaluate heap-condition of left-child
        except IndexError as _:
            pass
    if right_index <= last_index:
        try:
            if a[node_index] > a[right_index]:  # if node bigger than right-leaf:
                a[node_index], a[right_index] = a[right_index], a[node_index]  # switch them around
                heap_seepin(a, right_index, last_index)  # re-evaluate heap-condition of right-child
        except IndexError as _:
            pass
    pprint_tree(a, "heap_seepin-")


def heapify(a: List[int]) -> None:
    """Heapify the array"""
    if is_heap(a):
        return

    for node_index in range(len(a) // 2, -1, -1):  # /2 => abgerundet | count downwards to incl. 0
        heap_seepin(a, node_index)
    pprint_tree(a)


def is_heap(a: List[int], i: int = 0) -> bool:
    """Checks whether the array is a heap(heap characteristic fulfilled) or not"""
    n = len(a)
    if i > int((n - 2) / 2):  # if leaf node return true, leafs can't break heap-condition
        return True

    # If i-node is smaller than its children, and same is
    # recursively true for the children, return True (else False)
    if (_get(a, i, math.inf) <= _get(a, 2 * i + 1, math.inf) and
            _get(a, i, math.inf) <= _get(a, 2 * i + 2, math.inf) and
            is_heap(a, 2 * i + 1) and is_heap(a, 2 * i + 2)):
        return True
    return False


def heapsort(a: List[int]) -> None:
    """Heapsort algorithm, sorts the array"""
    heapify(a)  # convert a to heap
    assert is_heap(a)
    last_element = len(a) - 1
    while last_element > 0:
        a[0], a[last_element] = a[last_element], a[0]
        heap_seepin(a, 0, last_element - 1)
        last_element -= 1


def height(i: int) -> int:
    """Returns the height of the heap at index i"""
    return int(math.log(1 + i, 2))


def print_as_tree(a: List[int]) -> None:
    """Prints an array as a tree like structure"""
    left = lambda i: i * 2 + 1
    right = lambda i: i * 2 + 2

    for i, _ in enumerate(a):
        left_child = left(i)
        right_child = right(i)
        print("\tcurrent Node:%s(%s, %s):" % (_get(a, i),
                                              height(i),
                                              height(left(i)) - height(right(i))), end="")
        if _get(a, left_child) is not None:
            print("%s(%s, %s)" % (_get(a, left_child),
                                  height(left_child),
                                  height(left(left_child)) - height(right(left_child))), end="")
        else:
            print("None, ", end="")

        if _get(a, right_child) is not None:
            print("%s(%s, %s)" % (_get(a, right_child),
                                  height(right_child),
                                  height(left(right_child)) - height(right(right_child))))
        else:
            print("None")
        i += 1


def pprint_tree(a, title=""):
    """ Prints array tree like with a title"""

    print(title, end="")
    print("Tree: \n\tArray: %s" % a)
    print_as_tree(a)


if __name__ == "__main__":
    pprint_tree(MY_ARRAY, "unsorted/unheapified-")
    print("heapify: ")
    heapify(MY_ARRAY)
    print("heap-array: %s" % MY_ARRAY)
    print("is_heap: %s" % is_heap(MY_ARRAY))
    print("heapsort: ")
    heapsort(MY_ARRAY)
    print("sorted: %s" % MY_ARRAY)

    SORTED_ARRAY = MY_ARRAY.copy()  # check if really sorted:
    SORTED_ARRAY.sort(reverse=True)
    assert list(MY_ARRAY) == SORTED_ARRAY
