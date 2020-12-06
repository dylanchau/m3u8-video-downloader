# Reqirement modules: re, request and pycryptodome
import re
import requests
from Crypto.Cipher import AES

def get_decrypt_key(key_url_pattern, m3u8_content):
    k = re.compile(key_url_pattern)
    
    key_url = k.findall(m3u8_content.text)[0]
    key_content = requests.get(key_url).content

    # decrypt, new has three parameters,
    # The first is the binary data of the key (key),
    #
    # The third IV will be given after the URI in the m3u8 file. If not, you can try to assign the key to the IV.
    sprytor = AES.new(key_content, AES.MODE_CBC, IV=key_content)

    return sprytor


def get_ts_list(ts_url_pattern, m3u8_content):
    url_pattern = re.compile(ts_url_pattern)
    ts_urls = url_pattern.findall(m3u8_content.text)

    return ts_urls


def download_ts(ts_urls, decrypt_key, save_path):

    for url in ts_urls:
        ts_name = url.split('/')[-1]

        print("Downloading:" + ts_name)
        ts = requests.get(url).content

        # The cipher text length is not a multiple of 16, then add b"0" until the length is a multiple of 16.
        # while len(ts) % 16 != 0:
        #     ts += b'0'

        print("Decrypting:" + ts_name)
        with open(f'./videos/{save_path}.ts', 'ab') as f:
            # # decrypt method parameter needs to be a multiple of 16, if not, you need to add binary "0"
            f.write(decrypt_key.decrypt(ts))


if __name__ == "__main__":
    m3u8_link = input('The M3U8 URL:')
    save_path = input('The video name:')

    text = requests.get(m3u8_link)

    ''' 
        complie the pattern URI of script used to decrypt and encrypt
        E.g. http://decrypt_encrypt_script.[bin|key|...]. https://.*?\.bin
    '''
    decrypt_script = get_decrypt_key(r'https://.*?\.bin', text)

    ''' 
        complie the pattern of videos link
        E.g. http://video_1.[html|ts|...]. https://.*?\.html
    '''
    ts_links = get_ts_list(r'https://.*?\.html', text)

    download_ts(ts_links, decrypt_script, save_path)

    print(f'{save_path} download completed')
