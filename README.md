# ether_transact
Python + java + rabbitMQ implementation for sending and receiving ether

# JAVA

Listens for incoming blocks in the node and triggers Observable method which is subscribed as an event

Subscription subscription = web3j.blockObservable(false).subscribe(block -> {

//Call wallet update apis

});

# PYTHON

Has apis to createwallet,getbalance and sendTransaction 
walletUpdate api is triggred when a new block is added to the node and it sends the new block number to rabbitMQ queue which checks if the incoming transactions in the block has same to address as the addresses created in the node. 


