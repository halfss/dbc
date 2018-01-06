import json
import tornado.web

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
            "amount": 1
          }
        }

        '''
        print "memary trans len is %s" % len(self.state.trans)
        print self.state.trans
        trans = json.loads(self.request.body.decode('utf-8'))
        transable, return_trans = transfer.transfer_check(trans)
        if not transable:
            self.write({'result':'failed'})
            return
        print "trans check result: %s" % transable
        print "New transaction:"
        print "  From %s to %s" % (trans['from'], trans['to'])
        for k, v in trans['assets'].items():
            print "\t%s%s transfer from %s to %s" % (v, k, trans['from'], trans['to'])
        self.trans(trans)
        return_utxo=''
        if return_trans:
            return_utxo = self.trans(return_trans)
        print "new memary trans len is %s" % len(self.state.trans)
        print self.state.trans
        self.write(json.dumps({"result":"success", "return_utxo":return_utxo}))

    def trans(self, trans):
        self.state.trans_add(trans)
        return transfer.transfer_hash(json.dumps(trans))
