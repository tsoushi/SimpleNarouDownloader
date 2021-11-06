import os
import time
import json
from selenium import webdriver
#from selenium.webdriver.support.select import Select

def main(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option('prefs', {'download.default_directory': os.getcwd()+os.sep+'download'})

    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://syosetu.com')
    if os.path.exists('cookies.json'):
        with open('cookies.json') as f:
            cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

    main_loop(driver)

    print('クッキーを保存しています')
    with open('cookies.json', 'w') as f:
        json.dump(driver.get_cookies(), f)
    print('ドライバーを終了しています')
    driver.quit()

R18_DOMAIN = 'https://novel18.syosetu.com'
NORMAL_DOMAIN = 'https://ncode.syosetu.com'

def main_loop(driver):
    ncode = None
    sleep = 5
    error_wait = 25
    domain = R18_DOMAIN
    while 1:
        cmd = input('コマンド(help:h): ') 

        if cmd == 'h':
            print('''\
    quit
    login
    r18=true
    r18=false
    dl=1-10
    sleep=5
    error_wait=25
    ncode=N1111aa''')
        
        if cmd == 'login':
            driver.get('https://ssl.syosetu.com/login/input/')
        if cmd == 'quit':
            return
        if cmd == 'r18=false':
            domain = NORMAL_DOMAIN
        if cmd == 'r18=true':
            domain = R18_DOMAIN

        try:
            if cmd.startswith('ncode'):
                ncode = cmd.split('=')[1]
                print('ncodeを[{}]にセット'.format(ncode))

            if cmd.startswith('sleep'):
                sleep = int(cmd.split('=')[1])

            if cmd.startswith('error_wait'):
                error_wait = int(cmd.split('=')[1])
        except (ValueError, IndexError):
            print('値が正しくありません')
            continue

        if cmd.startswith('dl'):
            try:
                start, end = cmd.split('=')[1].split('-')
                start = int(start)
                end = int(end)
            except (ValueError, IndexError):
                print('値が正しくありません')
                continue
            for i in range(start, end+1):
                try:
                    while 1:
                        driver.get(domain+'/txtdownload/dlstart/ncode/{ncode}/?no={no}&hankaku=0&code=utf-8&kaigyo=crlf'.format(ncode=ncode, no=i))
                        print(i)
                        if 'エラーが発生しました' in driver.page_source:
                            print('エラーが発生したため待機中({}秒)'.format(error_wait))
                            wait(5)
                            driver.get(domain+'/txtdownload/top/ncode/{ncode}'.format(ncode=ncode))
                            wait(error_wait - 5)
                            continue
                        break
                    if i != end:
                        wait(sleep)
                except KeyboardInterrupt:
                    print('ダウンロードを中止')
                    break

def wait(sec):
    for i in range(sec):
        print('\r'+'wait:'+str(sec-i)+' '*3, end='')
        time.sleep(1)
    print('\r'+' '*10+'\r', end='')
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--noheadless', '-n', action='store_false', help='ヘッドレスモードで起動しない')
    args = parser.parse_args()
    main(args.noheadless)
