import json
import tornado.web

from dbc.api.base import TBCHandle

class Transaction(tornado.web.RequestHandler):
    def initialize(self, state):
        self.state = state

    def post(self):
        '''
        transaction data:
        {
            "from": account,
            "to": account,
            "assets":{"money": 4, "usd": 5} #this is a custom json
        }
        '''
        trans = json.loads(self.request.body.decode('utf-8'))
        print "New transaction:"
        print "  From %s to %s" % (trans['from'], trans['to'])
        for k, v in trans['assets'].items():
            print "\t%s%s transfer from %s to %s" % (v, k, trans['from'], trans['to'])
        print "Transaction END"
        self.state.trans_add(trans)
        self.write(json.dumps({"result":"success"}))
