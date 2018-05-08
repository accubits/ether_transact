# ether_transact
Python + java + rabbitMQ implementation for sending and receiving ether

To receive all new blocks as they are added to the blockchain (the false parameter specifies that we only want the blocks, not the embedded transactions too)
Subscription subscription = web3j.blockObservable(false).subscribe(block -> {
    ...
});
