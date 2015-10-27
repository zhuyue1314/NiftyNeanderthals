#!/usr/bin/python
# Pull the certificate info from our JSON output

import argparse
import sys
import json
from os.path import basename
import re


def get_cert_info(INFILE, ipaddr, ip_cert):
    print "\nCheck: " + ip_cert
    with open(INFILE, 'r') as fh:
        jsondata = json.load(fh)

    return jsondata[ipaddr]["subjects"][ip_cert]["values"]


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


def get_ip_certs(INFILE, ipaddr):
    """Get a list of certs associated with an IP"""
    print "[Checking] : " + ipaddr,
    with open(INFILE, 'r') as fh:
        jsondata = json.load(fh)
        certs = jsondata[ipaddr]["certificates"]
        print "[" + str(len(certs)) + "]"

    return certs


def parse_input(INPUTFILE, OUTPUTFILE):
    """Read our JSON file"""
    print "Reading: " + INPUTFILE
    with open(INPUTFILE, 'r') as fh:
        data = json.load(fh)

    TSUBNET = basename(INPUTFILE)
    TEMP = TSUBNET.split('.')
    SUBNET = str(TEMP[0]) + "." + str(TEMP[1]) + "." + str(TEMP[2])
    ips = pull_ips(INPUTFILE, SUBNET)
    for ipaddr in ips:
        ip_certs = get_ip_certs(INPUTFILE, ipaddr)
        for ip_cert in ip_certs:
            output = get_cert_info(INPUTFILE, ipaddr, ip_cert)
            print output
            with open(OUTPUTFILE, 'a') as fh:
                fh.write(str(output))
                fh.write("\n")


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Pull SSL/TLS info from file')
    parser.add_argument('--input-file', '-i', dest='inputfile', help='Read this file')
    parser.add_argument('--output-file', '-o', dest='outputfile', default='results.txt', help='Write output to this file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    INPUTFILE = args.inputfile
    OUTPUTFILE = args.outputfile

    if not args.inputfile:
        sys.exit(parser.print_help())
    else:
        parse_input(INPUTFILE, OUTPUTFILE)


if __name__ == '__main__':
    __main__()
