# dbc
`a data block chain implement by python`

# Implemented
* block chain pack
* node sync

# to do
* transaction check
* coin publication

## API
###1: transaction
```
curl -X POST
     http://localhost:8080/transaction
     -d '{
     		"from":"1EAB87F6-ADEE-4D02-97D6-1FABA205EA7C",
     		"to":"A140FBB8-524D-41BC-A07A-EFDCFF18756D",
     		"assets":{"money":3}
     }'
```

###2: mine:
```
 curl  http://localhost:8080/mine
```
###3: block
* 1: get last block

	```
	curl http://localhost:8080/block
	```

* 2: get block by id

	```
	curl http://localhost:8080/block/7
	```
