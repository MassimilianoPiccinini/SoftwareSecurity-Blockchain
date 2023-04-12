from tkinter import filedialog
from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from solcx import install_solc
install_solc(version='latest')
from solcx import compile_source
import subprocess
import os
import tkinter as tk
from PIL import Image, ImageTk
import threading
import json

onChainSmartContract = None
web3_1 = None
web3_2 = None
web3_3 = None
web3_4 = None

def start_blockchains():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.call(['bash', os.path.join(current_dir, "init.sh")])

def get_sc(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, filename), 'r') as file:
        text = file.read()
    return text

def update_storage(map):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'onchaindata.json')
    try:
        with open(filename, 'r') as file:
            maps = json.load(file)
    except FileNotFoundError:
        maps = []
    maps.append(map)
    with open(filename, 'w') as file:
        json.dump(maps, file)

def read_storage(name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'onchaindata.json')
    with open(filename, 'r') as file:
        maps = json.load(file)
    for map_data in maps:
        if map_data['name'] == name:
            return map_data
    return None

def deploy(w3: Web3, contract: Contract, name: str):
    sm_transaction = {
        "from": w3.eth.accounts[0],
        "gas": w3.to_hex(6721975),
        "gasPrice": w3.to_wei('0', 'gwei'),
        "nonce": w3.eth.get_transaction_count(w3.eth.accounts[0]),
        "data": contract.bytecode
    }
    signedTransaction = w3.eth.account.sign_transaction(sm_transaction, "0x4f11e05b6908439852b5ea7c97da15738dfadd111b3fc89d4c812423fa929b45")
    transaction_hash = w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=contract.abi, bytecode=contract.bytecode)
    new_map = {
        'name': name,
        'address': str(contract.address),
        'abi': str(contract.abi)
    }
    update_storage(new_map)
    return contract

def read(contract: Contract, function_name: str, args: list):
    if len(args) == 0:
        # result = contract.functions.askForDeploySmartContract().call()
        result = contract.functions[function_name]().call()
    elif len(args) == 1:
        result = contract.functions[function_name](args[0]).call()
    elif len(args) == 2:
        result = contract.functions[function_name](args[0], args[1]).call()
    else:
        result = contract.functions[function_name](args[0], args[1], args[2]).call()
    return result

def write(w3: Web3, contract: Contract, function_name: str, args: any):
    new_transaction = {
        "from": w3.eth.accounts[0],
        "to": contract.address,
        "data": contract.encodeABI(fn_name=function_name, args=args),
        "gas": w3.to_hex(6721975),
        "gasPrice": w3.to_wei('0', 'gwei'),
        "nonce": w3.eth.get_transaction_count(w3.eth.accounts[0])
    }
    signedTransaction = w3.eth.account.sign_transaction(new_transaction, "0x4f11e05b6908439852b5ea7c97da15738dfadd111b3fc89d4c812423fa929b45")
    transaction_hash = w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    return receipt

def init_web3():
    global web3_1
    global web3_2
    global web3_3
    global web3_4
    web3_1 = Web3(HTTPProvider("http://127.0.0.1:8545"))
    if web3_1.is_connected():
        print("Connected to http://127.0.0.1:8545")
    else:
        print("Not connected to http://127.0.0.1:8545")
    web3_2 = Web3(HTTPProvider("http://127.0.0.1:8546"))
    if web3_2.is_connected():
        print("Connected to http://127.0.0.1:8546")
    else:
        print("Not connected to http://127.0.0.1:8546")
    web3_3 = Web3(HTTPProvider("http://127.0.0.1:8547"))
    if web3_3.is_connected():
        print("Connected to http://127.0.0.1:8547")
    else:
        print("Not connected to http://127.0.0.1:8547")
    web3_4 = Web3(HTTPProvider("http://127.0.0.1:8548"))
    if web3_4.is_connected():
        print("Connected to http://127.0.0.1:8548")
    else:
        print("Not connected to http://127.0.0.1:8548")

def loadOnChainManager():
    compiledSmartContract = compile_source(get_sc("onchainmanager.sol"), output_values=['abi', 'bin'])
    _, smartContractInterface = compiledSmartContract.popitem()
    smartContractBytecode = smartContractInterface['bin']
    smartContractAbi = smartContractInterface['abi']
    global onChainSmartContract
    onChainSmartContract = web3_1.eth.contract(abi=smartContractAbi, bytecode=smartContractBytecode)
    count = web3_1.eth.get_transaction_count(web3_1.eth.accounts[0])
    sc = read_storage("onchainsc")
    if sc is None:
        onChainSmartContract = deploy(web3_1, onChainSmartContract, 'onchainsc')
        # my_contract = web3_1.eth.contract(address=onChainSmartContract.address, abi=onChainSmartContract.abi)
    else:
        onChainSmartContract = web3_1.eth.contract(address=sc["address"], abi=smartContractAbi, bytecode=smartContractBytecode)
    
    write(web3_1, onChainSmartContract, 'setAddress1', ["http://127.0.0.1:8546"])
    write(web3_1, onChainSmartContract, 'setAddress2', ["http://127.0.0.1:8547"])
    write(web3_1, onChainSmartContract, 'setAddress3', ["http://127.0.0.1:8548"])

class Loader(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.title("Progetto Software Security & Blockchain")
        self.result_text = tk.Text(self)
        tk.Button(self, text="Avvia le Blockchain", command=self.run_script_threaded).grid(row=1, column=0)
        tk.Button(self, text="Avvia il Programma", command=self.start_app).grid(row=1, column=1)
        self.result_text.grid(row=2, column=0, columnspan=2)

    def run_script_threaded(self):
        threading.Thread(target=self.run_script).start()
        # threading.Thread(target=self.init_web3_thread).start()

    def start_app(self):
        # self.result_text.insert(tk.END, "Tutte le Blockchain sono state inizializzate correttamente!")
        # self.result_text.insert(tk.END, "Caricamento del programma... (impiega circa 15 secondi)")
        homepage = HomePage(self.master)
        init_web3()
        loadOnChainManager()

    def run_script(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        command = ['bash', os.path.join(current_dir, "init.sh")]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            self.result_text.insert(tk.END, output)
            self.result_text.see(tk.END)

class HomePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//4}+{screen_height//4}")
        self.title("Home Page")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        button1_image = Image.open(os.path.join(current_dir, "receipt_long.png"))
        button2_image = Image.open(os.path.join(current_dir, "assignment.png"))
        button3_image = Image.open(os.path.join(current_dir, "tty.png"))
        button1_photo = ImageTk.PhotoImage(button1_image)
        button2_photo = ImageTk.PhotoImage(button2_image)
        button3_photo = ImageTk.PhotoImage(button3_image)

        title_label = tk.Label(self, text="Scegli come deployare il tuo smart contract, oppure se richiamare un metodo di uno smart contract esistente.", font=("Arial", 13))
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        button1 = tk.Button(self, image=button1_photo, text="Deploy file .sol", compound=tk.TOP, font=("Arial", 12), command=self.button1_clicked)
        button1.image = button1_photo
        button1.grid(row=1, column=0, padx=0, pady=10)
        frame1 = tk.Frame(self, height=100, width=100)
        frame1.pack_propagate(0)
        frame1.grid(row=2, column=0, padx=0, pady=10)
        label1 = tk.Label(frame1, text="Carica il tuo\nfile in solidity\nin cui è scritto\nlo Smart Contract", font=("Arial", 13))
        label1.pack(fill=tk.BOTH, expand=1)

        button2 = tk.Button(self, image=button2_photo, text="Deploy da ABI e Bytecode", compound=tk.TOP, font=("Arial", 12), command=self.button2_clicked)
        button2.image = button2_photo
        button2.grid(row=1, column=1, padx=0, pady=10)
        frame2 = tk.Frame(self, height=100, width=100)
        frame2.pack_propagate(0)
        frame2.grid(row=2, column=1, padx=0, pady=10)
        label2 = tk.Label(frame2, text="Carica il tuo\nSmart Contract\nscrivendo l'ABI\ne il Bytecode", font=("Arial", 13))
        label2.pack(fill=tk.BOTH, expand=1)

        button3 = tk.Button(self, image=button3_photo, text="Chiama metodo", compound=tk.TOP, font=("Arial", 12), command=self.button3_clicked)
        button3.image = button3_photo
        button3.grid(row=1, column=2, padx=0, pady=10)
        frame3 = tk.Frame(self, height=100, width=100)
        frame3.pack_propagate(0)
        frame3.grid(row=2, column=2, padx=0, pady=10)
        label3 = tk.Label(frame3, text="Chiama un\nmetodo di uno\nSmart Contract\nesistente", font=("Arial", 13))
        label3.pack(fill=tk.BOTH, expand=1)

    def get_folder_path():
        while True:
            folder_path = input("Please enter the path of the folder: ")
            if os.path.isdir(folder_path):
                return folder_path
            else:
                print("Invalid folder path. Please try again.")

    def button1_clicked(self):
        soliditypage = SolidityPage(self.master)

    def button2_clicked(self):
        abibytecodepage = ABIBytecodePage(self.master)

    def button3_clicked(self):
        callmethodpage = MethodsPage(self.master)

class SolidityPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//4}+{screen_height//4}")
        self.title("Deploy file .sol")
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        self.file_label = tk.Label(self, text="File:")
        self.file_label.pack()
        
        self.file_entry = tk.Entry(self, state="readonly")
        self.file_entry.pack()
        
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.pack()
        
        self.ok_button = tk.Button(self, text="OK", command=self.ok_button_click)
        self.ok_button.pack(side=tk.LEFT)
        
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_button_click)
        self.cancel_button.pack(side=tk.LEFT)

    def browse_file(self):
        filetypes = (("Solidity files", "*.sol"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.file_entry.config(state="readonly")
        
    def ok_button_click(self):
        name = self.name_entry.get()
        filename = self.file_entry.get()
        if not filename.endswith(".sol"):
            tk.messagebox.showerror("Error", "Invalid file format. Please select a .sol file.")
        else:
            compiledSmartContract = compile_source(get_sc(os.path.basename(filename).split('/')[-1]), output_values=['abi', 'bin'])
            _, smartContractInterface = compiledSmartContract.popitem()
            smartContractBytecode = smartContractInterface['bin']
            smartContractAbi = smartContractInterface['abi']
            receipt = write(web3_1, onChainSmartContract, "getNextAddress", [])
            logs = onChainSmartContract.events.NextAddressReturned().process_receipt(receipt)
            nextAddress = logs[0]['args']['nextAddress']
            web3_c = Web3(HTTPProvider(nextAddress))
            if web3_c.is_connected():
                print("Connected to " + nextAddress)
                customSmartContract = web3_c.eth.contract(abi=smartContractAbi, bytecode=smartContractBytecode)
                customSmartContract = deploy(web3_c, customSmartContract, name)
                write(web3_1, onChainSmartContract, 'addContract', [name, str(nextAddress), str(customSmartContract.address), str(smartContractAbi)])
                result = read(onChainSmartContract, 'getContract', [name])
                print("Result: " + str(result))
            else:
                print("Not connected to " + nextAddress)

            self.destroy()
        
    def cancel_button_click(self):
        self.destroy()

class ABIBytecodePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//4}+{screen_height//4}")
        self.title("Deploy da ABI e Bytecode")
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        self.abi_label = tk.Label(self, text="ABI:")
        self.abi_label.pack()
        
        self.abi_label = tk.Entry(self)
        self.abi_label.pack()
        
        self.bytecode_label = tk.Label(self, text="Bytecode:")
        self.bytecode_label.pack()
        
        self.bytecode_label = tk.Entry(self)
        self.bytecode_label.pack()
        
        self.ok_button = tk.Button(self, text="OK", command=self.ok_button_click)
        self.ok_button.pack(side=tk.LEFT)
        
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_button_click)
        self.cancel_button.pack(side=tk.LEFT)
        
    def ok_button_click(self):
        name = self.name_entry.get()
        smartContractAbi = self.abi_label.get()
        smartContractBytecode = self.bytecode_label.get()
        receipt = write(web3_1, onChainSmartContract, "getNextAddress", [])
        logs = onChainSmartContract.events.NextAddressReturned().process_receipt(receipt)
        nextAddress = logs[0]['args']['nextAddress']
        web3_c = Web3(HTTPProvider(nextAddress))
        if web3_c.is_connected():
            print("Connected to " + nextAddress)
            customSmartContract = web3_c.eth.contract(abi=smartContractAbi, bytecode=smartContractBytecode)
            customSmartContract = deploy(web3_c, customSmartContract, name)
            write(web3_1, onChainSmartContract, 'addContract', [name, str(nextAddress), str(customSmartContract.address), str(smartContractAbi)])
            result = read(onChainSmartContract, 'getContract', [name])
            print("Result: " + str(result))
        else:
            print("Not connected to " + nextAddress)

        self.destroy()
        
    def cancel_button_click(self):
        self.destroy()

class MethodsPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//4}+{screen_height//4}")
        self.title("Chiama metodo")
        self.name_label = tk.Label(self, text="Name of the smart contract:")
        self.name_label.pack()
        
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        self.function_label = tk.Label(self, text="Function name:")
        self.function_label.pack()
        
        self.function_label = tk.Entry(self)
        self.function_label.pack()

        self.selected_option = tk.IntVar()
        self.selected_option.set(0)

        self.option1 = tk.Radiobutton(self, text='Lettura', variable=self.selected_option, value=0)
        self.option1.pack(padx=10)
        self.option2 = tk.Radiobutton(self, text='Scrittura', variable=self.selected_option, value=1)
        self.option2.pack(padx=10)
        
        self.arg1_label = tk.Label(self, text="Arg 1:")
        self.arg1_label.pack()
        
        self.arg1_label = tk.Entry(self)
        self.arg1_label.pack()

        self.arg2_label = tk.Label(self, text="Arg 2:")
        self.arg2_label.pack()
        
        self.arg2_label = tk.Entry(self)
        self.arg2_label.pack()

        self.arg3_label = tk.Label(self, text="Arg 3:")
        self.arg3_label.pack()
        
        self.arg3_label = tk.Entry(self)
        self.arg3_label.pack()
        
        self.ok_button = tk.Button(self, text="OK", command=self.ok_button_click)
        self.ok_button.pack(side=tk.LEFT)
        
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel_button_click)
        self.cancel_button.pack(side=tk.LEFT)
        
    def ok_button_click(self):
        selected_option = self.selected_option.get()
        name = self.name_entry.get()
        function = self.function_label.get()
        arg1 = self.arg1_label.get()
        arg2 = self.arg2_label.get()
        arg3 = self.arg3_label.get()
        data = read(onChainSmartContract, "getContract", [name])
        blockChainAddress = data[0]
        address = data[1]
        abi = data[2].replace("'", '"').replace('False', 'false').replace('True', 'true')
        web3_c = Web3(HTTPProvider(blockChainAddress))
        if web3_c.is_connected():
            print("Connected to " + blockChainAddress)
            customSmartContract = web3_c.eth.contract(address=address, abi=abi)
            if arg1 and arg2 and arg3:
                if selected_option == 0:
                    result = read(customSmartContract, function, [arg1, arg2, arg3])
                else:
                    write(web3_c, customSmartContract, function, [arg1, arg2, arg3])
            elif arg1 and arg2:
                if selected_option == 0:
                    result = read(customSmartContract, function, [arg1, arg2])
                else:
                    write(web3_c, customSmartContract, function, [arg1, arg2])
            elif arg1:
                if selected_option == 0:
                    result = read(customSmartContract, function, [arg1])
                else:
                    write(web3_c, customSmartContract, function, [arg1])
            else:
                if selected_option == 0:
                    result = read(customSmartContract, function, [])
                else:
                    write(web3_c, customSmartContract, function, [])
        else:
            print("Not connected to " + blockChainAddress)
        if selected_option == 0:
            self.show_toast('Dati ottenuti correttamente', str(result))
        else:
            self.show_toast('Dati scritti correttamente', '')
        self.destroy()
        
    def cancel_button_click(self):
        self.destroy()

    def show_toast(self, title, description):
        window = tk.Toplevel()
        window.overrideredirect(True)
        window.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window.geometry(f"{500}x{100}+{screen_width//2-50}+{screen_height//2-50}")

        # create a frame for the toast message
        frame = tk.Frame(window, bg='white', bd=1, relief=tk.RAISED)
        frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # create a label for the title and add it to the frame
        title_label = tk.Label(frame, text=title, font=('Arial', 14, 'bold'), fg='black', bg='white')
        title_label.pack(padx=10, pady=5)

        # create a label for the description and add it to the frame
        desc_label = tk.Label(frame, text=description, font=('Arial', 12), fg='gray', bg='white')
        desc_label.pack(padx=10, pady=5)

        # function to destroy the window after a short delay
        def destroy_window():
            window.after(3000, window.destroy)
        
        window.after(3000, destroy_window)

root = tk.Tk()
app = Loader(root)
app.pack()
root.mainloop()