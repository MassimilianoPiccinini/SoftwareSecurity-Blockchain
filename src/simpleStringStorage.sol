// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract Storage {

    string myString;

    /**
     * @dev Store value in variable
     * @param myStr value to store
     */
    function store(string memory myStr) public {
        myString = myStr;
    }

    /**
     * @dev Return value 
     * @return value of 'myString'
     */
    function retrieve() public view returns (string memory){
        return myString;
    }
}