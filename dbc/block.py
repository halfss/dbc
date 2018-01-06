#!/usr/bin/env python2.7
import os

import json
import hashlib
import time

from dbc import transfer
from dbc import utils

from dbc.options import get_options

tbc_opts = [
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
    },
    {
        "name": "block_zone_length",
        "default": 2,
        "help": "how many trans in one block",
        "type": int,
    }
    ]

options = get_options(tbc_opts, 'init')

class Block():
    '''
    define block structure and rule
    '''
    def __init__(self, index, timestamp, data, previous_hash, nonce='', bhash='', sync=False):
        self.data = data
        if type(data) != dict: return "Illegal data, data must be dict"
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.sync = sync
        if self.sync:
            self.nonce = nonce
            self.hash = bhash
        else:
            self.nonce, self.hash = self.get_nonce()

    def get_nonce(self):
        for i in range(0,10000000):
            i = str(i)
            block_hash_str = self.hash_block(i)
            print block_hash_str
            print block_hash_str[:options.block_zone_length]
            if block_hash_str[:options.block_zone_length] == '0' * options.block_zone_length:
                break
        return i, block_hash_str


    def hash_block(self, nonce):
        block_str = str(self.index) + \
                    str(self.timestamp) + \
                    str(self.data) + \
                    str(self.previous_hash) + \
                    nonce
        print block_str
        return self.block_hash(block_str)

    def dict(self):
        return dict(
                index = self.index,
                timestamp = self.timestamp,
                data = self.data,
                previous_hash = self.previous_hash,
                hash = self.hash,
                nonce = self.nonce
                )

    def block_hash(self, text):
        sha = hashlib.sha256()
        sha.update(text.encode('utf-8'))
        return sha.hexdigest()

    def check(self):
        block_file_name = options.block_path_format % (options.chain_dir, hex(self.dict()['index']))
        if os.path.isfile(block_file_name):
            print "block %s is exist, pass" % self.dict()['index']
            return False
        if self.sync:
            print "block content check"
            if self.hash != self.hash_block(self.nonce):
                print "hash is not correct, %s(send) != %s(generate)" % (self.hash, self.hash_block(self.nonce))
                return False
            previous_block = get_block_by_id(self.index-1)
            if self.previous_hash != previous_block['hash']:
                print "hash is not continuity"
                return False
            if self.data['trans'][0]['assets']['coin'] != utils.get_reward(self.index):
                print "reward is not correct"
                return False
        return True

    def save(self):
        '''
        save block file as a file to disk
        '''
        if not self.check():
            print "block check failed"
            return False
        block_file_name = options.block_path_format % (options.chain_dir, hex(self.dict()['index']))
        print "block %s trans is %s" % (self.dict()['index'], self.dict()['data']['trans'])
        for _trans in self.dict()['data']['trans']:
            print _trans
            transfer.transfer_save(json.dumps(_trans))
        block_file = file(block_file_name, 'w')
        block_file.write(str(json.dumps(self.dict())))
        file(options.block_path_format % (options.chain_dir, 'head'), 'w').write(json.dumps({"max":self.dict()['index']}))
        print "block %s is save with %s" % (self.dict()['index'], block_file_name)

def create_genesis_block(genesis_json):
    '''
    create the Gendsis Block
    '''
    data = {}
    alloc = genesis_json.get('alloc', {})
    if alloc:
        trans = []
        for k, v in alloc.items():
            _trans = {
                "from": 0,
                "to": k,
                "assets":v
                }
            print "intial alloc is: %s" % _trans
            trans.append(_trans)
            transfer.transfer_save(json.dumps(_trans))
        data['trans'] = trans
    data['info'] = genesis_json
    return Block(0, str(time.time()), data, "0")

def get_last_block():
    last_content = file(options.block_path_format % (options.chain_dir, 'head'), 'r').read()
    last_json = json.loads(last_content)
    last_id = last_json['max']
    return get_block_by_id(last_id)

def get_block_by_id(block_id):
    block_file_name = options.block_path_format % (options.chain_dir, str(hex(int(block_id))))
    block_content = file(block_file_name, 'r').read()
    return json.loads(block_content)
