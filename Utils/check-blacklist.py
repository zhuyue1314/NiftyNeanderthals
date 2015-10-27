#!/usr/bin/python
# Check our certificate files against a blacklist from Abuse.ch

# Usage: check-blacklist.py -f /data/145.0.2.0_24.json -i 145.0.2 -b /data/sslblacklist.csv

import argparse
import sys
import re
import json


def compare_hashes(ip_cert, bad_hashes):
    """Check if our hash appears on the blacklist"""
    # Uncomment this if you want to print the certificate being checked
    # print "Checking: " + ip_cert
    for badhash in bad_hashes:
        checkhash = badhash.split('-')[0]
        if ip_cert == checkhash:
            print "[WARNING] - [BAD CERTIFICATE] " + badhash
        else:
            pass


def get_ip_certs(INFILE, ipaddr):
    """Get a list of certs associated with an IP"""
    print "[Checking] : " + ipaddr,
    with open(INFILE, 'r') as fh:
        jsondata = json.load(fh)
        certs = jsondata[ipaddr]["certificates"]
        print "[" + str(len(certs)) + "]"

    return certs


def get_bad_cert_hashes(BLACKLIST):
    """Pull a list of bad hashes from Abuse.sh blacklist"""
    bad_hashes = []
    with open(BLACKLIST, 'r') as fh:
        for line in fh.readlines():
            certhash = line.split(',')[1]
            certbadness = line.split(',')[2]
            certinfo = certhash + "-" + certbadness
            bad_hashes.append(certinfo)

    return bad_hashes


def pull_ips(INFILE, IPRANGE):
    """Pull a list of valid IPs from file"""
    ips = []
    with open(INFILE, 'r') as fh:
        for line in fh:
            found = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
            if found:
                rawdata = str(found)

    ipdata = rawdata.split(',')

    for ip in ipdata:
        if IPRANGE in ip:
            newip = ip.split('\'')[1]
            ips.append(newip)
        else:
            pass

    return ips


def parse_input(INFILE, BLACKLIST, IPRANGE):
    """Parsing input file"""
    ips = pull_ips(INFILE, IPRANGE)
    bad_hashes = get_bad_cert_hashes(BLACKLIST)
    print "[INFO] Input file: " + INFILE
    print "[INFO] IP Range: " + IPRANGE
    print "[INFO] IP Addresses: " + str(len(ips))
    print "[INFO] Black list: " + BLACKLIST
    print "[INFO] Bad hashes: " + str(len(bad_hashes)) + "\n"

    for ipaddr in ips:
        ip_certs = get_ip_certs(INFILE, ipaddr)
        for ip_cert in ip_certs:
            hash_check = compare_hashes(ip_cert, bad_hashes)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Check our certificates against a blacklist')
    parser.add_argument('--input-file', '-f', dest='infile', help='Our certificate input file')
    parser.add_argument('--blacklist-file', '-b', dest='blacklist', help='Abuse.ch blacklist file')
    parser.add_argument('--ip-range', '-i', dest='iprange', help='IP Range in file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    INFILE = args.infile
    BLACKLIST = args.blacklist
    IPRANGE = args.iprange

    if not args.infile:
        sys.exit(parser.print_help())
    else:
        parse_input(INFILE, BLACKLIST, IPRANGE)


if __name__ == '__main__':
    __main__()
