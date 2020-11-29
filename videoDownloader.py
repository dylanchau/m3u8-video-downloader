# Reqirement modules: re, request and pycryptodome
import re
import requests
from Crypto.Cipher import AES

# The name of video file will be saved
name = 'test.mp4'
# m3u8 file url
url = 'https://abc.m3u8'

r = requests.get(url)
''' 
    complie the pattern URI of script used to decrypt and encrypt
    E.g. http://decrypt_encrypt_script.[bin|key|...]. https://.*?\.bin
'''
k = re.compile(r'https://.*?\.bin')
''' 
    complie the pattern of videos link
    E.g. http://video_1.[html|ts|...]. https://.*?\.html
'''
html = re.compile(r'https://.*?\.html')

key_url = k.findall(r.text)[0]
html_url = html.findall(r.text)

key_content = requests.get(key_url).content

# decrypt and save ts
for ts_url in html_url:
    ts_name = ts_url.split('/')[-1]

    # decrypt, new has three parameters,
    # The first is the binary data of the key (key),
    #
    # The third IV will be given after the URI in the m3u8 file. If not, you can try to assign the key to the IV.
    sprytor = AES.new(key_content, AES.MODE_CBC, IV=key_content)
    print("Downloading:" + ts_name)
    ts = requests.get(ts_url).content

    # The cipher text length is not a multiple of 16, then add b"0" until the length is a multiple of 16.
    # while len(ts) % 16 != 0:
    #     ts += b'0'

    print("Decrypting:" + ts_name)
    with open(name, 'ab') as f:
        # # decrypt method parameter needs to be a multiple of 16, if not, you need to add binary "0"
        f.write(sprytor.decrypt(ts))

print(name, "Download completed")