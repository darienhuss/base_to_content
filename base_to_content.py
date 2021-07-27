#!/usr/bin/python -tt
#Author: Darien Huss

import os
import sys
import base64
import string
import difflib
import argparse

def encode(string_to_encode,alphabet,standard_base,base32):
	if base32:
		encoded = base64.b32encode(string_to_encode)
	else:
		encoded = base64.b64encode(string_to_encode)
	return encoded.translate(string.maketrans(alphabet, standard_base))

def longest(a, b):
	match = difflib.SequenceMatcher(None, a, b)
	m = match.find_longest_match(0, len(a), 0, len(b))
	return a[m.a:m.a+m.size]

def main():
	parser = argparse.ArgumentParser(description='Create three possible base64 contents based on given string')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-s','--stringplain',help='Plaintext string')
	parser.add_argument('-c','--customalphabet',help='Specify a custom alphabet',required=False)
	parser.add_argument('-32','--base32',help='Use base32 instead of base64',action='store_true',required=False)
	parser.add_argument('-u','--unicode',help='String is unicode',action='store_true',required=False)
	group.add_argument('-in', '--input',help='Input a file to encode',type=argparse.FileType('r'))
	args = parser.parse_args()

	if args.stringplain:
		string_to_encode = args.stringplain
	elif args.input:
		string_to_encode = args.input.read()
		
	base32 = args.base32
	if base32:
		standard_base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567' #standard base32 alphabet
	else:
		standard_base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' #standard base64 alphabet

	if args.customalphabet:
		alphabet = args.customalphabet
		if len(alphabet) != len(standard_base):
			print 'Custom alphabet must be same length as standard alphabet, exiting...'
			sys.exit(1)
	else:
		alphabet = standard_base

	if args.unicode:
		string_tmp = ''
		for c in string_to_encode:
			string_tmp += '%s\x00' % c
		string_to_encode = string_tmp.rstrip('\x00')
		
	for t in [3, 4, 5]:
		init_string1 = encode(os.urandom(t) + string_to_encode + os.urandom(6),alphabet,standard_base,base32) #initialize first string
		for i in range(100):
			init_string2 = encode(os.urandom(t) + string_to_encode + os.urandom(6),alphabet,standard_base,base32)
			init_string1 = longest(init_string1, init_string2)
		print 'content:"' + init_string1 + '";'

if __name__ == '__main__':
  main()
