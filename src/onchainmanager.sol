// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

contract OnChainManager {
    
    struct Contract {
        string myAddress;
        string myAbi;
    }
    
    mapping(string => Contract) private _contracts;
    string private _address1;
    string private _address2;
    string private _address3;
    uint8 private _counter;
    
    function setAddress1(string memory address1) public {
        _address1 = address1;
    }
    
    function getAddress1() public view returns (string memory) {
        return _address1;
    }
    
    function setAddress2(string memory address2) public {
        _address2 = address2;
    }
    
    function getAddress2() public view returns (string memory) {
        return _address2;
    }
    
    function setAddress3(string memory address3) public {
        _address3 = address3;
    }
    
    function getAddress3() public view returns (string memory) {
        return _address3;
    }
    
    function addContract(string memory name, string memory myAddress, string memory myAbi) public {
        Contract memory newContract = Contract(myAddress, myAbi);
        _contracts[name] = newContract;
    }
    
    function getContract(string memory name) public view returns (string memory, string memory) {
        Contract memory contract_ = _contracts[name];
        return (contract_.myAddress, contract_.myAbi);
    }
    
    function deleteContract(string memory name) public {
        delete _contracts[name];
    }

    function setCounter(uint8 counter) public {
        //_counter = (counter + 1) % 3;
        _counter = counter + 1;
    }
    
    function getCounter() public view returns (uint8) {
        return _counter;
    }
    
    function getNextAddress() public returns (string memory, uint8) {
        string memory nextAddress = "";

        uint8 counter = getCounter();

        if (_counter == 0) {
            nextAddress = _address1;
        } else if (_counter == 1) {
            nextAddress = _address2;
        } else if (_counter == 2) {
            nextAddress = _address3;
        }

        setCounter(counter);

        return (nextAddress, _counter);
    }
}
