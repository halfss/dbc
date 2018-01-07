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
        if utxo['to'] != _addr: return (False, {})
        print "signout is pair or not"
        account.verify(trans['singout'], trans['publickey'], trans['from'])
    except:
        return (False, {})
    result, new_assets = transfer(trans, utxo)
    if result and new_assets:
        print "new assets after trans is %s" % new_assets
        utxo['to'] =trans.get('returto') or utxo['to']
        utxo['assets'] = new_assets
    else:
        utxo = {}
    os.remove(options.trans_path_format % (options.chain_dir, trans['from']))
    print "ddddddd:w"
    print utxo
    return (True, utxo)

def transfer(trans, utxo):
    print "trans assets: %s" % trans['assets']
    for k, v in trans['assets'].items():
        if float(v) > float(utxo['assets'].get(k, 0)):
            print "trans %s is large than %s" %s (v, utxo['assets'][k])
            return False, {}
        else:
            utxo['assets'][k] -= float(v)
    print utxo['assets']['coin']
    utxo['assets']['coin'] -= trans['fee']
    print utxo['assets']['coin']
    if utxo['assets']['coin'] < 0:
        print "utxo is not enouth to pay fee: %s" % utxo['assets']['coin']
        return False, {}
    for v in utxo['assets'].values():
        if v: return True, utxo['assets']

def get_utxo_by_id(trans):
    utxo_id = trans['from']
    utxo_str = file(options.trans_path_format % (options.chain_dir, utxo_id), 'r').read()
    return json.loads(utxo_str)
