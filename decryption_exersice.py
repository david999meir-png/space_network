my_txt = "r"
my_key = 5
real_txt = chr(ord(my_txt) ^ my_key)
print(real_txt)


original_text = "Secret"
key = 123
encrypted_text = ""

for char in original_text:
    temp = ord(char) ^ key
    encrypted_text+= chr(temp)

print(encrypted_text)


word1 = ""
for i in encrypted_text:
    temp = ord(i) ^ key
    word1 += chr(temp)
print(word1)

new_key = "ABC"
massage = "how are you?"

decryption_txt = ""
for i,v in enumerate(massage):
    temp = ord(v) ^ ord(new_key[i % len(new_key)])
    decryption_txt += chr(temp)

print(decryption_txt)