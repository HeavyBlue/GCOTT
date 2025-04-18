import hashlib

from random import shuffle


class PasswordCracker:
    """
    A class to crack hashed passwords using a provided wordlist.
    Supports MD5, SHA1, SHA256, and SHA512 hashing algorithms.
    Can process the wordlist in ordered or randomized fashion.
    """

    def __init__(self, hashed_password: str, password_list_path: str, hash_type: str = 'md5',
                 randomness: str = "ordered"):
        """
        Initializes the Password_Cracker object.

        Args:
            hashed_password (str): The target hashed password to crack.
            password_list_path (str): The path to the file containing the list of potential passwords.
            hash_type (str, optional): The hashing algorithm used (md5, sha1, sha256, sha512). Defaults to 'md5'.
            randomness (str, optional): Determines the order of password testing ('ordered' or 'random'). Defaults to 'ordered'.
        """
        self.hashed_password = hashed_password
        self.password_list = self._load_and_process_passwords(password_list_path, randomness)
        self.hash_type = hash_type.lower()
        self.randomness = randomness.lower()
        self._validate_hash_type()

    @staticmethod
    def _load_and_process_passwords(password_list_path: str, randomness: str) -> list[str]:
        """
        Loads passwords from the file and optionally shuffles them.

        Args:
            password_list_path (str): The path to the password list file.
            randomness (str): 'ordered' to keep the original order, 'random' to shuffle.

        Returns:
            list[str]: A list of passwords.
        """
        try:
            with open(password_list_path, "r", encoding="utf-8", errors="ignore") as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            raise FileNotFoundError(f"Password list file not found at: {password_list_path}")

        if randomness == "random":
            shuffle(password_list)
        return password_list

    def _validate_hash_type(self):
        """
        Validates if the provided hash type is supported.

        Raises:
            ValueError: If the hash type is not one of the supported algorithms.
        """
        supported_types = ["md5", "sha1", "sha256", "sha512"]
        if self.hash_type not in supported_types:
            raise ValueError(
                f"Unsupported hash type: {self.hash_type}. Supported types are: {', '.join(supported_types)}")

    def show(self):
        """
        Prints the list of passwords being used for cracking.
        """
        print(self.password_list)

    def crack(self) -> str:
        """
        Attempts to crack the hashed password by iterating through the password list
        and comparing the hash of each password with the target hash.

        Returns:
            str: The cracked password if found, otherwise "Password not found".
        """
        counter = 0
        for password in self.password_list:
            counter += 1
            hashed_attempt = self._hash_password(password)
            if hashed_attempt == self.hashed_password:
                print(f"{counter}. password tried")
                return password
        return "Password not found"

    def _hash_password(self, password: str) -> str:
        """
        Hashes the given password using the specified hashing algorithm.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hexadecimal representation of the hashed password.
        """
        encoded_password = password.encode()
        match self.hash_type:
            case "md5":
                return hashlib.md5(encoded_password).hexdigest()
            case "sha1":
                return hashlib.sha1(encoded_password).hexdigest()
            case "sha256":
                return hashlib.sha256(encoded_password).hexdigest()
            case "sha512":
                return hashlib.sha512(encoded_password).hexdigest()
            case _:
                raise ValueError(f"Unsupported hash type: {self.hash_type}")
