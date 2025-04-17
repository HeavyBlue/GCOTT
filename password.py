class Password_Cracker:
    def __init__(self, hashed_password, password_list_path, hash_type, randomness="ordered"):
        self.hashed_password = hashed_password
        with open(password_list_path, "r", encoding="utf-8", errors="ignore") as file:
            password_list = file.read().split("\n")
            if (randomness == "random"):
                import random
                random.shuffle(password_list)
        self.password_list = password_list
        self.hash_type = hash_type
        self.randomness = randomness

    def show(self):
        print(self.password_list)

    def crack(self):
        import hashlib
        counter = 0
        for password in self.password_list:
            counter += 1
            if self.hash_type == "md5":
                hashed = hashlib.md5(password.encode()).hexdigest()
            elif self.hash_type == "sha1":
                hashed = hashlib.sha1(password.encode()).hexdigest()
            elif self.hash_type == "sha256":
                hashed = hashlib.sha256(password.encode()).hexdigest()
            elif self.hash_type == "sha512":
                hashed = hashlib.sha512(password.encode()).hexdigest()
            if hashed == self.hashed_password:
                print(counter, ". password tried")
                return password
        return "Password not found"
