import sys
import os
import time
import json
import aiohttp
import concurrent.futures
from datetime import datetime, timedelta
import requests


class DumpHqGameMatches(object):

    def __init__(self, countrycode='us'):
        self.api_uri = 'https://hqbuff.com/api/'
        self.first_game = datetime(2018, 5, 8)
        self.current_path = os.getcwd()
        self.current_file_path = './hq_game_dump_' + countrycode + '.json'
        self.worker_threads = os.cpu_count() * 2 if os.cpu_count() is not None else 5

    def get_json_data(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return [url, response.json()]
        else:
            return ['','']

    def build_urls_map(self, country):
        urls_map = []

        today = datetime.today() - timedelta(days=1)
        while today.date() > (self.first_game.date() - timedelta(days=1)):
            urls_map.append(self.api_uri + country + '/' + today.strftime('%Y-%m-%d'))
            today = today - timedelta(days=1)

        return urls_map

    async def dump_game_data(self, country):

        json_data = []

        urls = self.build_urls_map(country)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.worker_threads) as executor:
            for result in executor.map(self.get_json_data, [url for url in urls]):
                if result[0] is not '':
                    print(f"Parsing data from {result[0]}")
                    json_data.append(result[1])

        with open(self.current_file_path, 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    def run(self):

        print(f'Running from {self.current_path}\n')
        print(f'Using {self.worker_threads} worker threads\n')

        print('Start fetching previous game data...')

        start = time.time()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.dump_game_data('us'))
        loop.close()

        end = time.time()

        print(f'\nParsing took : {end - start} seconds\n')


def main():
    args = sys.argv[1:]

    if len(args) < 1 or len(args) > 2 or '-cc' not in args and '--countrycode' not in args:
        print("Usage hq_data_dumper.py -cc [--countrycode][us, de, uk, au]")
    else:
        DumpHqGameMatches(args[1]).run()


if __name__ == "__main__":
    main()
