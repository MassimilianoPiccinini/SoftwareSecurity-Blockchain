pragma solidity ^0.8.0;

contract StringContract {
    string public storedString;

    function writeString(string memory value) public {
        storedString = value;
    }

    function updateString(string memory value) public {
        storedString = value;
    }

    function deleteString() public {
        delete storedString;
    }

    function readString() public view returns (string memory) {
        return storedString;
    }
}
