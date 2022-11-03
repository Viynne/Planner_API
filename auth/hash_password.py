from passlib.context import CryptContext


pass_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class HashPassword:

    def create_hash(self, password: str):
        return pass_context.hash(password)

    def verify_hash(self, plain_password: str, hash_password: str):
        return pass_context.verify(plain_password, hash_password)
