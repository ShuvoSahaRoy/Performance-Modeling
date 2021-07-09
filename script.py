import os, psutil
import os.path
import time
from Crypto import Random
from Crypto.Cipher import AES
from csv import DictWriter


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py' and fname!= 'output.csv'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)

def dir_size():
    total_dir_size = 0
    d = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(d):
        for f in files:
            file = os.path.join(root, f)
            total_dir_size += os.path.getsize(file)
    return total_dir_size/(1024**2)


def process_info():
    pid = os.getpid()
    py = psutil.Process(pid)
    cpu_utilization = py.cpu_percent()
    memory_utilization = py.memory_percent()
    mem = py.memory_percent()
    memory_usage = psutil.virtual_memory().total * (mem / 100) / (1024 ** 2)
    return cpu_utilization, memory_utilization, memory_usage


def system_info():
    cpu_in_use = psutil.cpu_percent()
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    memory_in_use = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_in_use, total_ram, memory_in_use, disk_usage


def csv_file(operation_type, timetaken):

    with open('output.csv', 'a', newline='') as f:
        csv_writer = DictWriter(f, fieldnames=['cpu_utlilization %', 'memory_utilization %', 'memory_usage MB','directory size MB','time_taken sec',
                                                'operation_type','total cpu in use %', 'total ram GB', 'ram in use %', 
                                                'disk_usage %'])
        if f.tell() == 0:
            csv_writer.writeheader()
        
        cpu_utilization, memory_utilization, memory_usage = process_info()
        cpu_in_use, total_ram, memory_in_use, disk_usage = system_info()
        if operation_type == 1:
            op = 'encription'
        else:
            op = 'decryption'
        time_taken = timetaken

        csv_writer.writerow({
            'cpu_utlilization %': cpu_utilization,
            'memory_utilization %':memory_utilization, 
            'memory_usage MB': memory_usage,
            'time_taken sec': time_taken,
            'directory size MB': str(dir_size()),
            'operation_type': op,
            'total cpu in use %': cpu_in_use, 
            'total ram GB': total_ram, 
            'ram in use %': memory_in_use, 
            'disk_usage %' : disk_usage,
        })


choice = int(input(
    "1. Press '1' to Encrypt all files in the directory.\n2. Press '2' to decrypt all files in the directory.\n3. Press '3' to exit.\n"))

if choice == 1:
    s_time = time.time()
    enc.encrypt_all_files()
    f_time = time.time() - s_time
    csv_file(1,f_time)

elif choice == 2:
    s_time = time.time()
    enc.decrypt_all_files()
    f_time = time.time() - s_time
    csv_file(2,f_time)
