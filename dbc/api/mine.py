import json
import time
import tornado.web

from dbc.block import get_block_by_id, get_last_block
from dbc.sync import sync
from dbc.options import get_options
options = get_options()

class Mine(tornado.web.RequestHandler):
    def initialize(self, state):
        self.state = state

    def get(self, block_id=''):
        '''
        watch transaction, if transaction is enough, start mining
        '''
        synced = sync(self.state)
        if len(self.state.trans) >= options.block_trans_size:
            self.state.block_pack()
