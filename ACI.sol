// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/*
 * @title ACI
 * @dev Manage cars
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract ACI {
    // Struct to store car information
    struct Car {
        string make;
        string model;
        uint year;
        uint price;
    }

    // Mapping to store all cars and their IDs
    mapping(uint => Car) cars;

    // Counter for car IDs
    uint carCounter = 0;

    uint[] public prices;
    uint public price;

    // Sell a car
    function sellCar(string memory _make, string memory _model, uint _year, uint _price) public {
        // Increment the car ID counter
        carCounter ++;

        // Store the car information in the mapping
        cars[carCounter] = Car(_make, _model, _year, _price);
    }

    // Search for a car
    function searchCar(string memory _make, string memory _model, uint _year) view  public returns (uint price) {
        // Iterate over all cars and search for a match
        for (uint i = 1; i <= carCounter; i++) {
            if (keccak256(abi.encodePacked(cars[i].make)) == keccak256(abi.encodePacked(_make)) || keccak256(abi.encodePacked(cars[i].model)) == keccak256(abi.encodePacked(_model)) || keccak256(abi.encodePacked(cars[i].year)) == keccak256(abi.encodePacked(_year))) {
                return cars[i].price;
            }
        }

        //return prices;
    }
}