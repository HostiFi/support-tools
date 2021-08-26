import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d','--domain', help='Domain name to redirect 80, 443 to 8443 for')
args = parser.parse_args()

os.system("rm /var/www/html/index.html")
os_cmd = """cat > /var/www/html/index.html << EOF
<meta http-equiv="refresh" content="0; URL='https://""" + args.domain + """:8443'" />
EOF
"""
os.system(os_cmd)
print("Port 80, 443 are now redirected to https://" + args.domain + ":8443")