# Ransomware
Generated a random 128 bit key (16 characters) using ascii characters.
• Find all .txt files on the victim’s computer and Encrypt the bytes of these files.
• Send that key back to the server.
• Infect by sending your compiled malware to a list of emails.
• Payload
a) Encrypt ALL .txt files on the system.
b) Use AES ECB for the encryption process with the random key
mentioned at the beginning.
c) Generate a Public/Private key-pair using RSA
d) Save the key used in (b) to desktop in a .key (normal text file but change the
extension to .key not to mistakenly re-encrypt it) format named "Key.key".
e) Encrypt the key used in (b) using the public key then save the encrypted key
to the desktop in a .key file format named "encryptedKey.key".
f) Save the generated Public/Private key pair (one key per line ,Public then
Private) in another .key file named "keyPair.key".
g) Send the encrypted key from (e) to the server.
h) A decryption function must be present and will decrypt all files when the
original key is entered.
Infection
a) You should add an infection mechanism that sends the .exe file to the emails
below.
b)Access the following csv , extract the emails from it then send
the .exe file to them
Interface
a) A prompt should popup (CLI or GUI) indicating that the encryption is in
progress when the .exe is executed.
b) After encrypting all txt files, the prompt will wait for a key input in order to
decrypt the files back. Ënter Key to decrypt"
