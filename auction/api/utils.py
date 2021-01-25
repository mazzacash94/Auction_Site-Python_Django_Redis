from web3 import Web3

# get hash from the json file and write it on the ethereum blockchain ropsten

def sendTransaction(message):

    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/cb3427bf216548ba96157079ddac0427'))
    address = "0x259f5D2843fc4a953B929789d8FfA07C84009286"
    privateKey = "0xb1c7ad5eaaf77dec2546b683e105b13531ab8106cc0053b9d3d39f4bef38aa90"
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(

        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')

    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)

    return txId