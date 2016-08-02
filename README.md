# base_to_content
Generate all possible base(32|64) results in the form of Suricata/Snort contents

Usage:
  -h, --help            show this help message and exit
  -s STRINGPLAIN, --stringplain STRINGPLAIN
                        Plaintext string
  -c CUSTOMALPHABET, --customalphabet CUSTOMALPHABET
                        Specify a custom alphabet
  -32, --base32         Use base32 instead of base64
  -u, --unicode         String is unicode

EXAMPLE:
python base_to_content.py -s "fubar"
OUTPUT:
content:"ZnViYX";
content:"Z1YmFy";
content:"mdWJhc";