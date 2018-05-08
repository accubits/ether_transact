# Created by PyCharm.
# User: shehin . F.N
# Date: 2/5/18
# Time: 12:07 PM

from celery import Celery
from web3 import Web3, HTTPProvider
import time
provider = HTTPProvider('http://127.0.0.1:8545')
web3 = Web3(provider)


celery_app = Celery('tasks', backend='amqp',broker='amqp://localhost')


NO_OF_CONFIRMATION=6

@celery_app.task
def celery_update_wallet(blockNumber):
    block=web3.eth.getBlock(int(blockNumber))
    if block:
        if block['transactions']:
            for trans in block['transactions']:
                trans_details=web3.eth.getTransaction(trans.hex())
                for current_address in web3.personal.listAccounts:
                    if current_address == trans_details['to']:
                        while True:
                            time.sleep(10)
                            print('current confirmation count for address :'+trans_details['to']+' '+str((int(web3.eth.blockNumber)-int(blockNumber))))
                            if (int(web3.eth.blockNumber)-int(blockNumber))>=int(NO_OF_CONFIRMATION):
                                print('i got cash baby '+trans_details['to'])
                                break
                            else:
                                continue
        return True
    else:
        return False
