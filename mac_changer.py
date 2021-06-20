#!/bin/python3
import re
import optparse
from termcolor import colored
import subprocess
import time
class main(object):
    def __init__(self):
        print()
        print("########################################")
        print("|                                      |")
        print(colored("|        WELCOME TO MAC CHANGER        |","green"))
        print("|                                      |")
        print("########################################")
        self.options=self.get_args()
        if self.options.interface:
            self.a=self.interface_checker(self.options)
        else:
            print()
            print(colored("[-] no interface specified","red"))
        if self.options.mac:
            self.b=self.mac_checker(self.options)
        else:
            print()
            print(colored("[-] no mac specified!","red"))
        if((self.options.interface)and(self.options.mac))and((self.a=="ok") and (self.b=="ok")):
            self.mac_changer(self.options)
            self.crossverify(self.options)
    def get_args(self):
        parser=optparse.OptionParser()
        parser.add_option("-i","--interface",dest="interface",help="interface to change mac address !!(please use format ww:ww:ww:ww:ww:ww)")
        parser.add_option("-m","--mac",dest="mac",help="specify the spoofed mac address!!")
        (options,arguments)=parser.parse_args()
        return options    
    def mac_checker(self,options):
        if re.fullmatch(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",options.mac):
            print()
            print(colored("[+] valid mac address detected!!","green"))
            time.sleep(1)
            print()
            return "ok"
        else:
            print()
            print(colored("[-] invalid mac address !!","red"))
            exit()
            time.sleep(1)
    def interface_checker(self,options):
            result=subprocess.run(["ifconfig", options.interface],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL).returncode
            if result == 1:
                print()
                print(colored("[-] invalid interface detected !!","red"))
                exit()
                time.sleep(1)
            else:
                if options.interface=="lo":
                    print()
                    print(colored("[-] could not change mac address for local host !!","red"))
                    exit()
                print()
                print(colored("[+] valid interface detected !!","green"))
                time.sleep(1)
                return "ok"
    def mac_changer(self,options):
        subprocess.call(["ifconfig", options.interface, "down"])
        x=subprocess.run(["ifconfig", options.interface, "hw","ether", options.mac],stderr=subprocess.DEVNULL).returncode
        if x==1:
            print(colored("[-] cannot assign this mac address","red"))
            exit()
            time.sleep(1)
            print()
        subprocess.call(["ifconfig", options.interface , "up"])
        print(colored("[*] trying to change mac address.....","blue"))
        time.sleep(1)
        print()
    def crossverify(self,options):
        new_mac_byte_object=subprocess.check_output(["ifconfig",options.interface])
        new_mac=str(new_mac_byte_object,'utf-8')
        re_result=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",new_mac)
        matchme=re_result.group(0)
        if matchme==options.mac:
            print(colored("[+] mac address changed successfully  !!","green"))
            print()
            print(colored(f"[>] current mac address : {matchme} ","magenta",attrs=['bold','dark']))
        else:
            print(colored("[-] getting error in changing mac address","red"))
            exit()

obj=main()

