import random

def generate_password():
    password = ""
    for _ in range(4):
        digit = random.randint(0, 9)
        password += str(digit)
    return password


password = generate_password()
print("비밀번호:", password)
