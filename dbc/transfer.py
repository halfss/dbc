import hashlib
import os
import json

from dbc import account
from dbc.log import LOG

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
    file(options.trans_path_format % (options.chain_dir, file_name), 'w').write(trans)
    return file_name

def transfer_hash(trans):
    sha = hashlib.sha256()
    sha.update(trans.encode('utf-8'))
    return sha.hexdigest()

def utxo_transfer(trans):
    try:
        utxo = get_utxo_by_id(trans)
        _addr = account.get_addr(trans['publickey'])
        if utxo['to'] != _addr:
            LOG.debug("address is pair or not, %s != %s" % (utxo['to'], _addr))
            return (False, {}, {})
        account.verify(trans['singout'], trans['publickey'], trans['from'])
    except:
        LOG.debug("signout is pair or not")
        return (False, {}, {})
    result, new_assets = transfer(trans, utxo)
    if result and new_assets:
        LOG.debug("new assets after trans is %s" % new_assets)
        utxo['to'] =trans.get('returto') or utxo['to']
        utxo['assets'] = new_assets
        fee = float(trans['fee'])/2
        trans[u'fee'] = utxo[u'fee'] = fee
    else:
        utxo = {}
    os.remove(options.trans_path_format % (options.chain_dir, trans['from']))
    return (True, trans, utxo)

def transfer(trans, utxo):
    LOG.debug("trans assets: %s" % trans['assets'])
    for k, v in trans['assets'].items():
        if float(v) > float(utxo['assets'].get(k, 0)):
            LOG.debug("trans %s is large than %s" %s (v, utxo['assets'][k]))
            return False, {}
        else:
            utxo['assets'][k] -= float(v)
    utxo['assets']['coin'] -= trans['fee']
    if utxo['assets']['coin'] < 0:
        LOG.debug("utxo is not enouth to pay fee: %s" % utxo['assets']['coin'])
        return False, {}
    for v in utxo['assets'].values():
        if v: return True, utxo['assets']

def get_utxo_by_id(trans):
    utxo_id = trans['from']
    utxo_str = file(options.trans_path_format % (options.chain_dir, utxo_id), 'r').read()
    return json.loads(utxo_str)
