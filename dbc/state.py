#coding=utf8
import datetime
import time

from dbc.options import get_options
from dbc.block import Block

options = get_options()

class State():
    def __init__(self, miner_address,
            block,
            trans,
            peer_nodes,
            mining):
        self.miner_address = miner_address
        self.block = block
        self.trans = trans
        self.mining = mining
        self.peer_nodes = peer_nodes

    def trans_add(self, trans):
        self.trans.append(trans)

    def block_pack(self):
        index = self.block['index'] + 1
        timestamp = str(time.time())
        data = {
                "trans": self.trans[:options.block_trans_size]
                }
        previous_hash = self.block['hash']
        print "old block"
        print self.block
        new_block = Block(index, timestamp, data, previous_hash)
        new_block.save()
        print "new block"
        print new_block.dict()
        self.data_refresh(new_block)

    def data_refresh(self, block):
        self.block = block.dict()
        self.trans = self.trans[options.block_trans_size:]
