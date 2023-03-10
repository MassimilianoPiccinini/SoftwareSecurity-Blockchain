import web3
from web3 import Web3
from web3.contract import Contract, ConciseContract
from solcx import install_solc
install_solc(version='latest')
from solcx import compile_source
import asyncio

def interact_with_smart_contract():
    # Connect to local blockchain using Web3
    w3 = Web3(web3.HTTPProvider('http://127.0.0.1:22000'))


    # Check if connection is successful
    if w3.isConnected():
        print("Successfully connected to local blockchain.")
    else:
        print("Connection to local blockchain failed.")
        return

    compiled_sol = compile_source("""
        // SPDX-License-Identifier: GPL-3.0

        pragma solidity ^0.8.0;
        contract SimpleStorage {

            uint public storedData;

            event Change(string message, uint newVal);

            constructor(uint initVal) {
                emit Change("initialized", initVal);
                storedData = initVal;
            }

            function set(uint x) public {
                emit Change("set", x);
                storedData = x;
            }

            function get() view public returns (uint retVal) {
                return storedData;
            }

        }""", output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    # Contract address on the blockchain
    contract_address = Web3.toChecksumAddress("0xe273fd8a6deb07c4bd7226e0ba05724dcb4bd38a")

    # Create a contract object
    contract = w3.eth.contract(contract_address, abi=abi, bytecode=bytecode)

    # Call a method of the contract
    concise = ConciseContract(contract)
    result = concise.get()
    print("Address of contract method call:", result)

    blocks_number = w3.eth.getTransactionCount(w3.eth.accounts[0]) # get number of blocks of node (of blockchain)
    print(blocks_number)

    print(w3.eth.accounts[0])
    
    new_transaction = {
        "from": w3.eth.accounts[0],
        "to": contract_address,
        "data": contract.encodeABI(fn_name="set", args=[50]),
        "gas": w3.toHex(3737050400),
        "gasPrice": '0',
        "nonce": blocks_number
    }
    signedTransaction = w3.eth.signTransaction(new_transaction)
    sentTransaction = w3.eth.sendRawTransaction(signedTransaction.raw)
    print(sentTransaction)

# Call the function to interact with the smart contract
interact_with_smart_contract()