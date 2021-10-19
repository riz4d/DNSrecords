#!/usr/bin/python3

import sys
import subprocess
import argparse
import os
import re
import pathlib
from time import sleep
from termcolor import colored, cprint
from concurrent.futures import ThreadPoolExecutor

def banner():
    print("\033[91m")

    print("              ------------------------                                             ______")
    print("             /  |\    |\    |  -----  \                         |\_______________ (_____\\______________")
    print("            /   | \   | \   | /        \                HH======#H###############H#######################")
    print('           /    |  \  |  \  | ------    \                       \' ~""""""""""""""`##(_))#H\"""""Y########')
    print('          /     |  /  |   \ |      /     \                                       ))    \#H\       `"Y###')
    print('         /      | /   |    \| ----/       \                                      "      }#H)')
    print('        /      _____       _____           \                                                _')
    print('       /       (  *  )     (  *  )          \                    _ __ ___  ___ ___  _ __ __| |___')
    print("      /                                      \                   | '__/ _ \/ __/ _ \| '__/ _` / __|")
    print('      \          ___________________          /                  | | |  __/ (_| (_) | | | (_| \__ \ ')
    print('       \        /___________________\        /                   |_|  \___|\___\___/|_|  \__,_|___/')
    print('        \                                   /                   ')
    print('         ----------------------------------- ')
    print('                                                                       codded by riz4d             ')

    print("Press Control+C to stop anytime\033[0m")

# Check args
def args():
    global subdomains_file
    parser = argparse.ArgumentParser()
    print("Usage example: python3 dead_records.py -w subdomains.txt -o1 dead.txt -o2 cname.txt\n")
    parser.add_argument('-w', help='path to the list of subdomain file (required)', required=True)
    parser.add_argument('-o1', help='found dead records output (required)', required=True)
    parser.add_argument('-o2', help="found CNAME's from dead records output (required)", required=True)
    args = parser.parse_args()

    subdomains_file = open(sys.argv[2], "r").readlines()

# filter_dns
def filter_dns(wordz):
    filtration = str(wordz)
    filt = "b'|Host|not found:|3|NXDOMAIN|\\n"
    filt1 = re.sub(filt, '', filtration)
    filt2 = filt1.replace("()", "")
    filt3 = filt2.replace('[" ', '').replace('"]', "")
    filt4 = filt3.replace("\\n'", "")
    formatted  = filt4.replace("\\", "\n").replace(" ", "")

    return formatted

# Find dead dns
def dead_check(subz):
    global show_dead
    try:
        for s in subz:
            cmd = "host " + s
            p = p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
            dead = p.stdout.read()

            if "not found" in str(dead):
                dead_temp = open("dead-temp.txt", "a+")
                dead_temp.write(str(dead))
            else:
                continue

        exist_check = pathlib.Path("dead-temp.txt")
        if exist_check.exists() == True:
            pass
        else:
            print("\033[91mNO DEAD RECORDS FOUND :(")
            sys.exit(1)

        cprint("\033[96m\033[4mFOUND DEAD RECORDS:\n\033[0m", attrs=['blink'])

        read_dead = open("dead-temp.txt", "r").readlines()
        show_dead = filter_dns(read_dead)
        print("\033[93m")

        return show_dead

    except KeyboardInterrupt:
        os.system("/usr/bin/rm dead-temp.txt")
        sys.exit(1)


# Make temp file
def CNAME_check(deadz):
    try:
        try:
            for d in deadz:
                cmd = "dig CNAME +short " + d
                p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
                check = p.stdout.read()

                if len(check) == 0:
                    print("\033[91m" + str(d), " --> \033[0m")

                else:
                    print("\033[92m\033[4m" + str(d) + "\033[0m" +  " --> " + "\033[92m\033[4m" + check.decode() + "\033[0m")
                    write_cname = open("cname-temp.txt", "a+")
                    cnamez = str(d) + " --> " + check.decode() + "\n"
                    write_cname.write(cnamez)
        except KeyboardInterrupt:
            os.system("/usr/bin/rm cname-temp.txt")
            sys.exit(1)

    except KeyboardInterrupt:
        os.system("/usr/bin/rm cname-temp.txt")
        sys.exit(1)

def output():
    if len(sys.argv) > 4:
        o1 = sys.argv[4]
        found_dead = open(o1, "w")
        found_dead.write(str(multithread()))

    os.system("/usr/bin/rm dead-temp.txt")

    cprint("\033[96m\033[4mCHECKING FOR CNAME's: \n\033[0m", attrs=['blink'])

    dead = show_dead.split("\n")
    dead.pop()
    CNAME_check(dead)

# write to temp file
def writeTemp():
    if len(sys.argv) > 5:
        o2 = sys.argv[6]
        cname_temp = open("cname-temp.txt", "r").readlines()
        found_dead_cnames = open(o2, "w")
        found_dead_cnames.write(str(cname_temp))

    os.system("/usr/bin/rm cname-temp.txt")

def multithread():
    executor = ThreadPoolExecutor(2)
    future = executor.submit(dead_check, subdomains_file)
    #print(future.result())
    print(future.result())

def output():
    if len(sys.argv) > 4:
        o1 = sys.argv[4]
        found_dead = open(o1, "w")
        found_dead.write(str(multithread()))

    os.system("/usr/bin/rm dead-temp.txt")

    cprint("\033[96m\033[4mCHECKING FOR CNAME's: \n\033[0m", attrs=['blink'])

    dead = show_dead.split("\n")
    dead.pop()
    CNAME_check(dead)

def main():
    args()
    banner()
    output()
    writeTemp()

try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print("Control + C detected\nExiting")
    exit(0)
