import hashlib
import os
import json

from dbc import account

from dbc.options import get_options

transfer_opts = [
    {
        "name": 'trans_path_format',
        "default": "%s/utxo/%s.json",
        "help": 'this will save trans as json by this path',
        "type": str,
    }
    ]

options = get_options(transfer_opts, 'init')

def transfer_save(trans):
    file_name = transfer_hash(trans)
    print "utxo id is:", file_name
    file(options.trans_path_format % (options.chain_dir, file_name), 'w').write(trans)
    return file_name

def transfer_hash(trans):
    sha = hashlib.sha256()
    sha.update(trans.encode('utf-8'))
    return sha.hexdigest()

def transfer_check(trans):
    try:
        utxo = get_utxo_by_id(trans)
        _addr = account.get_addr(trans['publickey'])
        print "address is pair or not"
        print utxo['to'], _addr
        if utxo['to'] != _addr: return (False, {})
        print "signout is pair or not"
        account.verify(trans['singout'], trans['publickey'], trans['from'])
    except:
        return (False, {})
    new_assets = transfer(trans, utxo)
    print "new assets after trans is %s" % new_assets
    print new_assets
    if new_assets:
        utxo['to'] =trans.get('returto') or utxo['to']
        utxo['assets'] = new_assets
    else:
        utxo = {}
    os.remove(options.trans_path_format % (options.chain_dir, trans['from']))
    return (True, utxo)


def transfer(trans, utxo):
    print "trans assets: %s" % trans['assets']
    for k, v in trans['assets'].items():
        if float(v) > float(utxo['assets'].get(k, 0)):
            return False
        else:
            utxo['assets'][k] -= float(v)
    for v in utxo['assets'].values():
        if v: return utxo['assets']

def get_utxo_by_id(trans):
    utxo_id = trans['from']
    utxo_str = file(options.trans_path_format % (options.chain_dir, utxo_id), 'r').read()
    return json.loads(utxo_str)
