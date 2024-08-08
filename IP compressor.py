# use this
base85chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'

def ip_to_b85(ip):
    # input in numbers
    parts = list(map(int, ip.split('.')))
    num = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    # output b85 magic
    b85 = []
    while num > 0:
        b85.append(base85chars[num % 85])
        num //= 85

    # return
    return ''.join(reversed(b85)) or '0'

def b85_to_ip(b85):
    # input in numbers
    num = 0
    for char in b85:
        num = num * 85 + base85chars.index(char)

    # output IP magic
    parts = [
        (num >> 24) & 0xFF,
        (num >> 16) & 0xFF,
        (num >> 8) & 0xFF,
        num & 0xFF
    ]

    # return
    return '.'.join(map(str, parts))
# console shit
def main():
    while True:
        print("Whatcu wanna do?")
        print("1. Encode IP")
        print("2. Decode IP")

        choice = input("1 or 2: ").strip()
        # choice 1
        if choice == '1':
            ip = input("Enter IPv4: ").strip()
            try:
                enc = ip_to_b85(ip)
                print(f"Compressed: {enc}")
            except Exception as e:
                print(f"Shit hit the fan: {e}")
        # choice 2
        elif choice == '2':
            enc = input("Enter compressed IP: ").strip()
            try:
                ip = b85_to_ip(enc)
                print(f"Decoded: {ip}")
            except Exception as e:
                print(f"Shit hit the fan: {e}")
        # fuck you        
        else:
            print("Dude... literally 2 options")
        
        while True:
            again = input("Reset? (y/n)").strip().lower()
            if again == 'n':
                return
            elif again == 'y':
                break
            else:
                print("You are dyslexic")
                again
# doohickey
if __name__ == "__main__":
    main()
