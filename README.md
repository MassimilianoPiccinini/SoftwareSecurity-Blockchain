# Smart Contract Deployment Tool

## Python-based tool for deploying and interacting with smart contracts using the Web3 library and Tkinter GUI framework.

The program allows users to:

Deploying a Smart Contract: The tool allows you to deploy a smart contract by providing either a Solidity file or the ABI (Application Binary Interface) and bytecode of the contract. You can specify a name for the contract and initiate the deployment process.

Calling Methods of an Existing Contract: Once a contract is deployed, you can interact with it by calling its methods. The program provides a dropdown list of deployed contracts, allowing you to select a contract and choose a method to call. You can provide any required arguments and execute the method.

Deleting a Smart Contract: If you want to remove a deployed contract from the blockchain, the tool offers a functionality to delete contracts. You can select a contract from the dropdown list and delete it, removing it permanently from the blockchain.

## List of functions

- Click on the "Deploy il file .sol" button to deploy a contract from a Solidity file.
Provide a name for the contract and browse for the Solidity file to deploy.
Click the "Deploy" button to deploy the contract.
Deploying from ABI and Bytecode:

- Click on the "Deploy da ABI e Bytecode" button to deploy a contract using its ABI and bytecode.
Provide a name for the contract and enter the ABI and bytecode in the respective fields.
Click the "Deploy" button to deploy the contract.
Calling a Method of an Existing Contract:

- Click on the "Chiama metodo" button to call a method of an existing smart contract.
Select the contract from the dropdown list and choose the method to call.
Provide the required arguments and click the "Call" button to execute the method.
Deleting a Smart Contract:

- Click on the "Elimina Smart Contract" button to delete a deployed contract.
Select the contract from the dropdown list and click the "Delete" button to remove the contract.
Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## Installation

### Prerequisites

Python 3.x

1. Clone the repository from GitHub:

```$ git clone https://github.com/MassimilianoPiccinini/SoftwareSecurity-Blockchain.git```

2. Navigate to the project directory:

```$ cd SoftwareSecurity-Blockchain```

3. Install the ganache command line interface:

```$ npm install ganache --global```

4. Install the dependencies using pip:

```$ pip install web3 tkinter py-solc-x Pillow python-dotenv```

5. Run the program:

```$ python offchain.py```

## Developers

- Piccinini Massimiliano (S1110841@studenti.univpm.it) - Matricola: S1110841 - GitHub: https://github.com/MassimilianoPiccinini
- Larocca Michele (S1113201@studenti.univpm.it) - Matricola: S1113201 - GitHub: https://github.com/ShadowWalker1411
- Longarini Lorenzo (S1110740@studenti.univpm.it) - Matricola: S1110740 - GitHub: https://github.com/LorenzoLongarini
- Alesi Mattia (S1114418@studenti.univpm.it) - Matricola: S1114418 - GitHub: https://github.com/alesimattia
- Dediu Alex (S1108807@studenti.univpm.it) - Matricola: S1108807 - GitHub: https://github.com/alexxdediu
