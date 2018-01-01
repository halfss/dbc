#!/usr/bin/env python2.7
import os

import hashlib
import json
import time

from dbc.options import get_options

tbc_opts = [
    {
        "name": 'chain_dir',
        "default": "./data",
        "help": 'all chain data store in this dir',
        "type": str,
    },
    {
        "name": "block_path_format",
        "default": "%s/block/%s.json",
        "help": "the path to save block file in python format",
        "type": str,
    },
    {
        "name": "block_trans_size",
        "default": 5,
        "help": "how many trans in one block",
        "type": int,
    }
    ]

options = get_options(tbc_opts, 'init')

class Block():
    '''
    define block structure and rule
    '''
    def __init__(self, index, timestamp, data, previous_hash):
        self.data = data
        if type(data) != dict: return "Illegal data, data must be dict"
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.hash_block().encode('utf8')

    def hash_block(self):
        block_str = str(self.index) + \
                    str(self.timestamp) + \
                    str(self.data) + \
                    str(self.previous_hash)
        return self.block_hash(block_str)

    def dict(self):
        return dict(
                index = self.index,
                timestamp = self.timestamp,
                data = self.data,
                previous_hash = self.previous_hash,
                hash = self.hash
                )

    def block_hash(self, text):
        sha = hashlib.sha512()
        sha.update(text.encode('utf-8'))
        return sha.hexdigest()

    def check(self):
        block_file_name = options.block_path_format % (options.chain_dir, hex(self.dict()['index']))
        if os.path.isfile(block_file_name):
            print "block %s is exist, pass" % self.dict()['index']
            return False
        return True

    def save(self):
        '''
        save block file as a file to disk
        '''
        if not self.check(): return False
        block_file_name = options.block_path_format % (options.chain_dir, hex(self.dict()['index']))
        block_file = file(block_file_name, 'w')
        block_file.write(str(json.dumps(self.dict())))
        file(options.block_path_format % (options.chain_dir, 'head'), 'w').write(json.dumps({"max":self.dict()['index']}))

def create_genesis_block(genesis_json):
    '''
    create the Gendsis Block
    '''
    return Block(0, str(time.time()), genesis_json, "0")

def get_last_block():
    last_content = file(options.block_path_format % (options.chain_dir, 'head'), 'r').read()
    last_json = json.loads(last_content)
    last_id = last_json['max']
    return get_block_by_id(last_id)

def get_block_by_id(block_id):
    block_file_name = options.block_path_format % (options.chain_dir, '0x'+str(block_id))
    block_content = file(block_file_name, 'r').read()
    return json.loads(block_content)
