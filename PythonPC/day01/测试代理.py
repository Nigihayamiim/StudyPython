import telnetlib

if __name__ == '__main__':
    try:
        telnetlib.Telnet('106.4.212.228', port='65000', timeout=3)
    except:
        print('ip无效！')
    else:
        print('ip有效！')