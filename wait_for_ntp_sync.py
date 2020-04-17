import random
from itertools import cycle
from time import ctime, sleep

import ntplib


def main():
    ntp_servers = [
        'time.google.com',
        'pool.ntp.org',
        '0.resinio.pool.ntp.org',
        '1.resinio.pool.ntp.org',
        '2.resinio.pool.ntp.org',
        '3.resinio.pool.ntp.org'
    ]
    ntp_rr = cycle(ntp_servers)

    for ntp_server in ntp_rr:
        client = ntplib.NTPClient()
        try:
            response = client.request(ntp_server, version=4)
            offset = response.offset
            if abs(offset) < 300:
                print('NTP time sync offset within 300s at {}s'.format(offset))
                break
        except ntplib.NTPException as ntpe:
            delay = random.randrange(0, 5)
            print('Checking with {} fail, trying another one in {}s...'.format(ntp_server, delay))
            sleep(delay)

if __name__ == "__main__":
    main()
