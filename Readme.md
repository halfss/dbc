# dbc
`a light, high scalability blockchain implement`

#code
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          15            103             49            670
Markdown                         1             10              0             48
JSON                             1              0              0             11
-------------------------------------------------------------------------------
SUM:                            17            113             49            729
-------------------------------------------------------------------------------

# Implemented
* block chain pack
* node sync
* transaction check
* coin publication
* transfer fee
* log file support

# to do
* smart contact support

# API
* 1: transaction
```
curl -X POST
     http://localhost:8080/transaction
     -d '{
            "from": utxo,
            "to": u"5TFCyzyXAVw7fkEynnNvcN6HYFakwkX7wq",
            "publickey": "9772954e3275e571aef9d1.......89ae54c372c0",
            "singout": signout,
            "returto": "4tQ5RQERhFb3fJiqhJceZNhGhbWxyH5gxx",
            "fee": 0.0001,
            "assets": {u"coin": 20}
     }'
```

* 2: mine:
```
 curl  http://localhost:8080/mine
```
* 3: block
** 1: get last block

	```
	curl http://localhost:8080/block
	```

** 2: get block by id

	```
	curl http://localhost:8080/block/7
	```
*4: Account
** 1: get a private key

	```
	curl -X POST http://localhost:8080/account
	```

** 2: get a public key and addr by private key

	```
	curl http://localhost:8080/$private_key_hex
	```
