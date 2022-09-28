import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
from mnem_key import nmeonic



def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# Write down the address, private key, and the passphrase for later usage
generate_algorand_keypair()
# generate mnemonic adress from the dev account provided by sandbox 
mnemonic_1=nmeonic['mnemonic_1']
pub_key1= mnemonic.to_public_key(mnemonic_1)
priv_key1= mnemonic.to_private_key(mnemonic_1)

def first_transaction(private_key,my_address):
    address= "http://localhost:4001"
    token="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client=algod.AlgodClient(token,address)

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
    
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = address
    note = "Hello World".encode()
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(pub_key1, params, receiver, amount, None, note)
    # sign transaction with the 
    signed_txn = unsigned_txn.sign(priv_key1)
    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))
    # wait for confirmation 
    account_info = algod_client.account_info(address)
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 
        
    
first_transaction(priv_key1,pub_key1)