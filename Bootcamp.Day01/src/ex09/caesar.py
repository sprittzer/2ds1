import sys


def caesar_cipher(text, shift, mode='encode'):
    result = []
    
    for char in text:
        if 'а' <= char <= 'я' or 'А' <= char <= 'Я' or 'ё' in char or 'Ё' in char:
            raise Exception('The script does not support your language yet')
        
        if 'a' <= char <= 'z':
            base = ord('a')
            current = ord(char) - base
            if mode == 'encode':
                new_char = chr((current + shift) % 26 + base)
            else:
                new_char = chr((current - shift) % 26 + base)
            result.append(new_char)
        
        elif 'A' <= char <= 'Z':
            base = ord('A')
            current = ord(char) - base
            if mode == 'encode':
                new_char = chr((current + shift) % 26 + base)
            else:
                new_char = chr((current - shift) % 26 + base)
            result.append(new_char)
        
        else:
            result.append(char)
    
    return ''.join(result)


def main():
    if len(sys.argv) != 4:
        raise Exception('Usage: python3 caesar.py <encode|decode> <text> <shift>')
    
    mode = sys.argv[1]
    text = sys.argv[2]
    
    shift = int(sys.argv[3])
    
    if mode not in ['encode', 'decode']:
        raise Exception("Mode must be 'encode' or 'decode'")
    
    try:
        result = caesar_cipher(text, shift, mode)
        print(result)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()