#!/usr/local/bin/python3

# Author Andrés J. Moreno - TheGoodHacker

from pwn import *
from colorama import Fore, Style, init
from time import sleep

import re
import argparse
import sys
import signal
import requests
import urllib

def handler(sig, frame):
    print("\n\nQuitting.. ")
    sys.exit(1)

def definitions():
    #colors
    global info, fail, close, success 
    info, fail, close, success = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + Style.BRIGHT
    
    global menti_url, url_votes, url_identifiers, agent
    menti_url = "https://www.menti.com/"
    url_votes = menti_url+"core/votes/" 
    url_identifiers = menti_url+"core/identifiers"
    agent = 'Mozilla/5.0 (Android 5.1.1; Tablet; rv:61.0.2) Gecko/61.0.2 Firefox/61.0.2'

def banner():
    banner = r'''
    ███╗   ███╗███████╗███╗   ██╗████████╗██╗██████╗  ██████╗ ████████╗
    ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██║██╔══██╗██╔═══██╗╚══██╔══╝
    ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ██║██████╔╝██║   ██║   ██║   
    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██║██╔══██╗██║   ██║   ██║   
    ██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║██████╔╝╚██████╔╝   ██║   
    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═════╝  ╚═════╝    ╚═╝
    -------------------------------------------------------------------
                  Mentibot 1.0.0 - Mentimeter voting bot          
                Andrés J. Moreno - thegoodhackertv@gmail.com   
                      mentibot.py -h to get started 
    '''
    print(info+banner+close)

def arg_parse():
    example = 'Example:\n\n'
    example += '$ python3 mentibot.py -u https://www.menti.com/012345abcde -s 10 -r 40'
    # fix: show full help when run without args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=banner(), epilog=example)
    parser.add_argument('-u', metavar="URL", dest='url', default='', help="Mentimeter voting url", required=True)
    parser.add_argument('-s', metavar="SCORE", dest='score', default='', help="Score to send", required=True)
    parser.add_argument('-r', metavar="ROUNDS", dest='rounds', default='', help="Number of rounds", type=int, required=True)
    parser.add_argument('--no-banner',dest='nobanner', default=False ,help="Hide banner from output", action="store_true")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args

def main():
    global ok
    headers = {
        'User-Agent': agent 
    }
    json = {
        "question_type":"wordcloud",
        "vote": args.score
    }
    path = urllib.parse.urlparse(args.url).path[1:] 
    main_url = menti_url+path
    s = requests.session()
    r = s.get(main_url, headers=headers)
    public_key = re.findall(r'"public_key\\":\\"(.*?)\\"',r.text)[0]
    r = s.post(url_identifiers,headers=headers)
    identifier = re.findall(r'identifier":"(.*?)"',r.text)[0]
    
    headers2 = {
        'X-Identifier': identifier,
        'User-Agent': agent 
    }

    cookies = r.cookies.get_dict()
    r = s.post(url_votes+public_key, headers=headers2, cookies=cookies,json=json)
    ok = (r.status_code == 200)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    try:
        init()
        definitions()
        args = arg_parse()
        if not args.nobanner:
            banner()
        rounds = args.rounds
        counter = 1
        log.info(f"Starting Mentibot at {time.ctime()}\n\n")
        p = log.progress("Bot Working")
        for i in range(rounds):
            p.status(f"Sending score {args.score} - ({counter}/{rounds})")
            main()
            if ok:
                counter+=1
        p.success("Done!")
        log.info(f"Completed at {time.ctime()}\n")
    except KeyboardInterrupt:
        print(fail+'\n[-] User Interrupt. [-]')
        sys.exit(1)
