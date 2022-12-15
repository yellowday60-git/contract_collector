import requests
from bs4 import BeautifulSoup
import csv
import os


def address_parser(_target):
    RES = []
    RESULTS = "results.csv"
    ETH = "https://etherscan.io/"
    BSC = "https://bscscan.com/"
    POL = "https://polygonscan.com/"
    
    ARB = "https://arbiscan.io/"

    #not surpport
    AVA = "https://avascan.info/"
    OPT = "https://optimistic.etherscan.io/"
    target = ""

    if _target == "ETH":
        target = ETH
    elif _target == "BSC":
        target = BSC
    elif _target == "POL":
        target = POL
    elif _target == "ARB":
        target = ARB
    elif _target == "AVA":
        target = AVA
    elif _target == "OPT":
        print("not surpport yet")
        return RES
    else:
        print("ETH BSC POL ARB AVA OPT")

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        }

    url = target

    #<div class="d-flex justify-content-between">
    #mCSB_1_container > div:nth-child(1) > div.col-sm-8 > div > div.text-nowrap > a

    html = requests.get(url= url, headers = headers)
    sess = requests.Session()
    # print(html.text)

    bs = BeautifulSoup(html.text, 'html.parser')
    txns = "" 

    for link in bs.find_all('a'):
        if link.get("href") == None:
            continue
        if  "txs?block=" in link.get("href"):
            txns = link.get("href")
            break

    # print("####")
    # print(txns)

    ##/tx/0x61ccaaa229134a772b06d656b2e13f82d238c66b22e7ea0041c2f4a05556b192
    url = target + txns[1:]
    # print(url)
    html = requests.get(url= url, headers = headers)
    sess = requests.Session()
    # print(html.text)

    bs = BeautifulSoup(html.text, 'html.parser')
    txs = []

    for link in bs.find_all('a'):
        if link.get("href") == None:
            continue
        if "/tx/0x" in link.get("href"):
            txs.append(link.get("href"))
        
    # print(txs)
    for tx in txs:
        try:
            url = target + tx[1:]
            
            print("tx : " + url)
            html = requests.get(url= url, headers = headers)
            sess = requests.Session()
            
            bs = BeautifulSoup(html.text, 'html.parser')
            contract = ""
            
            contract = bs.find("a", {"id" : "contractCopy"})
            print("contract : " + contract.get('href'))
            
            address = contract.get('href')[9:]
            print(address)
            
            RES.append(address)
            
            # cmd = "slither address"
            # os.system(cmd)
            
        except:
            continue
        
    return RES
    
def main():
    address_parser("AVA")

if __name__ == "__main__":
	main()