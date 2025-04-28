import json
import os
from cryptography.fernet import Fernet


class DB(dict):
    def __init__(self, file: str = None):
        self.file = file
        self.key = b'Fq6ZI-s0oj5MAH7RcY82yUzAHWvuPKlhYy5l5LQW4gw='

        if not file:
            self.file = "db.txt"

        self.__base_data = {
            "host" : {
                "user" : "root",
                "passwd" : "root",
                "port" : 3306,
            }
        }

        if not os.path.exists(self.file):
            #if file not exits, create new one
            self.write(refresh = True)

        self.read()
        
    def read(self) -> dict:
        with open(self.file, "rb") as ff:
            try:
                self.update(json.loads(self.decrypt_data(ff.read())))
                return self
            except:
                print("ErrorInDataBase: Can't read it..")
                return self.write(refresh = True)
            

    def write(self, refresh = False) -> dict:
        if refresh:
            self.update(self.__base_data)

        with open(self.file, "wb") as tf:
            data = json.dumps(self)
            data = self.encrypt_data(data.encode())
            tf.write(data)

    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.write()

    def encrypt_data(self, data):
        f = Fernet(self.key)
        encrypted = f.encrypt(data)
        return encrypted
    
    def decrypt_data(self, data):
        f = Fernet(self.key)
        decrypted = f.decrypt(data)
        return decrypted.decode()

if __name__ == "__main__":
    d = DB()
    # d["20-01-2025"] = 10
    print(d)