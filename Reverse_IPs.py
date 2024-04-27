import requests
import os
import re
from multiprocessing.dummy import Pool as ThreadPool

def reverse_ip_domain_lookup(ip_address):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'
        }
        print(f"\t\tAttempting to connect to api.reverseipdomain.com for IP {ip_address}")
        response = requests.get(f'https://api.reverseipdomain.com/?ip={ip_address}', headers=headers, timeout=30).text
        if 'Domain Name' in response:
            regex = re.findall('<a href="/domain/(.*?)">', response)
            for domain_name in regex:
                website_url = 'http://' + domain_name
                print(f"\t\tFound website URL: {website_url}")
                with open('Reversed_IPs.txt', 'a') as file:
                    file.write(website_url + '\n')
        else:
            print(f"\t\tNo domain names found for IP {ip_address}.")
    except Exception as e:
        print(f"\t\tError processing IP {ip_address} with api.reverseipdomain.com: {e}")

def rapid_dns_lookup(ip_address):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'
        }
        print(f"\t\tAttempting to connect to rapiddns.io for IP {ip_address}")
        response = requests.get(f'https://rapiddns.io/s/{ip_address}?full=1&down=1#result/', headers=headers, timeout=30).text
        if '<th scope="row ">' in response:
            regex = re.findall(r'<td>(?!-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z]{1,63}</td>', response)
            for domain_name in regex:
                website_url = 'http://' + domain_name.replace('<td>', '').replace('</td>', '').replace('ftp.', '').replace('images.', '').replace('cpanel.', '').replace('cpcalendars.', '').replace('cpcontacts.', '').replace('webmail.', '').replace('webdisk.', '').replace('hostmaster.', '').replace('mail.', '').replace('ns1.', '').replace('ns2.', '').replace('autodiscover.', '')
                print("\t\tFound website URL: {}".format(website_url))
                with open('Reversed_IPs.txt', 'a') as file:
                    file.write(website_url + '\n')
        else:
            print(f"\t\tNo data found for IP {ip_address} on rapiddns.io.")
    except Exception as e:
        print(f"\t\tError processing IP {ip_address} with rapiddns.io: {e}")

def full_reverse_ip_lookup(ip_address):
    print(f"\t\tStarting lookups for IP: {ip_address}")
    rapid_dns_lookup(ip_address)
    reverse_ip_domain_lookup(ip_address)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
\t\t   ___                             _______    
\t\t  / _ \___ _  _____ _______ ___   /  _/ _ \___
\t\t / , _/ -_) |/ / -_) __(_-</ -_) _/ // ___(_-<
\t\t/_/|_|\__/|___/\__/_/ /___/\__/ /___/_/  /___/
                                              
                    {Updated Version}                                                                                                      
\t\tTelegram Channel Link : t.me/Ev3l_m0rty_Channel / Telegram Admin Link: t.me/Ev3l_m0rty''')
    print("\t\tStarting the Reverse IP Lookup Tool...")
    try:
        ip_list_file = input("\t\tEnter the path to your list of IPs: ")
        with open(ip_list_file, 'r') as file:
            ip_addresses = file.read().splitlines()
        num_threads = input("\t\tEnter the number of threads: ")
        pool = ThreadPool(int(num_threads))
        print(f"\t\tProcessing {len(ip_addresses)} IPs with {num_threads} threads...")
        pool.map(full_reverse_ip_lookup, ip_addresses)
    except Exception as e:
        print(f"\t\tAn error occurred during setup: {e}")

if __name__ == '__main__':
    main()
