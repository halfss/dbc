import json
import tornado.web

from dbc.block import get_block_by_id, get_last_block

class Block(tornado.web.RequestHandler):
    def initialize(self, state):
        self.state = state

    def get(self, block_id=''):
        '''
        get block, return block info by id
        '''
        if block_id:
            block_json = get_block_by_id(block_id)
        else:
            block_json = get_last_block()
        self.write(block_json)
