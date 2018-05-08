
# Created by PyCharm.
# User: shehin . F.N
# Date: 2/5/18
# Time: 12:07 PM

from web3 import Web3, HTTPProvider
from flask import Flask,request,jsonify
from tasks import celery_app,celery_update_wallet

provider = HTTPProvider('http://127.0.0.1:8545')
web3 = Web3(provider)
app = Flask(__name__)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route("/updateWallet",methods = ['POST', 'GET'])
def updateWallet():
    req = request.form.to_dict(flat=True)
    result = celery_update_wallet.delay(req['blockNumber'])
    data = {
        'success': True,
        'status_code': '200',
        'message': 'Sucessfully updated wallet',
        'result': req['blockNumber']

    }
    print(data)
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/createWallet",methods = ['POST', 'GET'])
def createWallet():
    req = request.form.to_dict(flat=True)
    account=web3.personal.newAccount(req['password'])
    data = {
        'success': True,
        'status_code': '200',
        'message': 'wallet created successfully',
        'result': str(account)
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/getBalance",methods = ['POST', 'GET'])
def getBalance():
    req = request.form.to_dict(flat=True)
    balace_wei=web3.eth.getBalance(web3.toChecksumAddress(str(req['address'])))
    data = {
        'success': True,
        'status_code': '200',
        'message': 'Balance in wei',
        'result': str(balace_wei)

    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@app.route("/sendTransaction",methods = ['POST', 'GET'])
def sendTransaction():
    req = request.form.to_dict(flat=True)
    status=False

    try:
        status=web3.personal.unlockAccount(web3.toChecksumAddress(req['from_address']), req['password'])

        balace_wei = web3.eth.getBalance(web3.toChecksumAddress(str(req['from_address'])))
        if balace_wei >= int(int(req['value']) +int(web3.eth.gasPrice)):
            tx = web3.eth.sendTransaction({'to': web3.toChecksumAddress(req['to_address']),
                                           'from': web3.toChecksumAddress(req['from_address']),
                                           'value': req['value']})


        if status is True:
            data = {
                'success': True,
                'status_code': '200',
                'message': 'Transaction created sucessfully',
                'result': tx.hex()
            }
            resp = jsonify(data)
            resp.status_code = 200

        else:
            data = {
                'success': True,
                'status_code': '412',
                'message': 'Precondition failed',
                'result': []
            }
            resp = jsonify(data)
            resp.status_code = 412

        return resp

    except Exception as ex :
        data = {
            'success': True,
            'status_code': '412',
            'message': 'Account password invalid',
            'result': []
        }
        resp = jsonify(data)
        resp.status_code = 200
        return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0')




