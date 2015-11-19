# Wavelet tree module; this data structure is static so it does not support inserts and deletions.

import logging

def Node:
    def __init__(self, bmap=None, left=None, right=None):
        self.bmap = bmap
        self.left = left
        self.right = right

    def set_bmap(self, bmap=None):
        if (bmap is None):
            logging.warn('No bitmap specified.')
            return
        self.bmap = bmap

    def get_bmap(self):
        return self.bmap

    def set_left(self, left=None):
        if (left is None):
            logging.warn('No node specified for insertion.')
            return
        self.left = left

    def get_left(self):
        return self.left

    def set_right(self, right=None):
        if (right is None):
            logging.warn('No node specified for insertion.')
            return
        self.right = right

    def get_right(self):
        return self.right


def WaveletTree:
    def __init__(self, string):
        if (string is None):
            logging.error('No string specified.')
            return
        self.string = string
        self.root = Node(bmap) # Todo: change bmap to reflect @string
