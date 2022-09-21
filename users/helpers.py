import bcrypt

def pass2hash(passwd):
    bytes = passwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash