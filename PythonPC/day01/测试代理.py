import telnetlib

if __name__ == '__main__':
    try:
        telnetlib.Telnet('171.35.50.18', port='8118', timeout=3)
    except:
        print('ip无效！')
    else:
        print('ip有效！')