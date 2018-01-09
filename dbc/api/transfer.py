import json
import tornado.web
from decimal import Decimal

from dbc import transfer

class Transfer(tornado.web.RequestHandler):
    def initialize(self, state):
        self.state = state

    def post(self):
        '''
        transaction data:
        {
          "from": "6453cbef347928491159770529f4a8b64de410eca353c8d20ca7eef7f5f214e7", #utxo hash
          "to": "5NRKJc2QHkHk7vhmSamW9UEDeYUoWLQJW8", # address to pay
          "publickey": "", # account's public key
          "singout": "", # hash sign by account private key
          "returnto": "8rP4v7r7bfpyo2XGHjP1wCanvVqDgZFrp4", #Remaining assets back address
          "assets": {
            "coin": 1
          }
        }

        '''
        LOG.debug("memary trans len is %s" % len(self.state.trans))
        LOG.debug(self.state.trans)
        trans = json.loads(self.request.body.decode('utf-8'))
        transable, trans, return_trans = transfer.utxo_transfer(trans)
        if not transable:
            LOG.debug("trans check result: %s" % transable)
            self.write({'result':'failed'})
            return
        LOG.debug("  From %s to %s" % (trans['from'], trans['to']))
        for k, v in trans['assets'].items():
            LOG.debug("\t%s%s transfer from %s to %s" % (v, k, trans['from'], trans['to']))
        return_utxo = self.trans(trans, return_trans)
        LOG.debug("new memary trans len is %s" % len(self.state.trans))
        LOG.debug(self.state.trans)
        self.write(json.dumps({"result":"success", "return_utxo":return_utxo}))

    def trans(self, trans, return_trans):
        self.state.trans_add({"trans": trans, "return": return_trans})
        return transfer.transfer_hash(json.dumps(return_trans))
