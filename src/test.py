import unittest
from unittest import mock
import offchain
from web3 import Web3
from offchain import update_storage, write


class offchainTestCase(unittest.TestCase):

    def test_ok_button_click(self):
        # qui mettiamo il path al nostro file
        with mock.patch("tkinter.filedialog.askopenfilename", return_value="/path/to/file.sol"):
            offchain.browse_file()
        offchain.name_entry.insert(0, "MyContract")
        offchain.ok_button.invoke()
        self.assertEqual(
            offchain.page.master.create_contract_from_file.call_count, 1)
        offchain.page.master.create_contract_from_file.assert_called_with(
            "MyContract", "/path/to/file.sol")

    def test_deploy_contract(self):
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        with open('metto qui il mio', 'r') as abi_definition:
            abi = abi_definition.read()
        with open('metto qui il mio', 'r') as bytecode_file:
            bytecode = bytecode_file.read()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        name = "metto il nome che darò"
        offchain.deploy(w3, contract, name)
        # controllo che il contratto sia stato creato correttamente
        self.assertIsNotNone(contract.address)
        # controllo che il nome del contratto sia stato salvato correttamente
        expected_map = {'name': name, 'address': str(
            contract.address), 'abi': abi}
        self.assertIn(expected_map, update_storage())


class TestWrite(unittest.TestCase):
    def setUp(self):
        self.w3 = Web3(Web3.TestRPCProvider())
        self.contract = self.w3.eth.contract(
            address='0x5B38Da6a701c568545dCfcB03FcB875f56beddC4',
            # abi=[<qui mettiamo il nostro abi>]
        )

    def test_write(self):
        result = write(self.w3, self.contract, 'setAddress1', 'prova')
        self.assertIsNotNone(result)
        self.assertIn('transactionHash', result)
        self.assertIn('transactionIndex', result)
        self.assertIn('blockHash', result)
        self.assertIn('blockNumber', result)
        self.assertIn('gasUsed', result)
        self.assertIn('status', result)
