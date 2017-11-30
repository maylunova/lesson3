with open("referat.txt", "r", encoding='utf-8') as f:
    string = ''.join(f)
    print(len(string.split()))