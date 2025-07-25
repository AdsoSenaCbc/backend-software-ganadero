from werkzeug.security import generate_password_hash
new_hash = generate_password_hash('juan123', method='pbkdf2:sha256', salt_length=16)
print(new_hash)