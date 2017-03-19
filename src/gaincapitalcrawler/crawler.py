import requests
import os
from os_utils import download, extract_and_merge

months = ['January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December']

def leading_zeros_string(x, digit_num):
    x_str = str(x)
    x_str_length = len(x_str)
    x_str = '0'*(digit_num - x_str_length) + x_str

    return x_str

class GCDataDownloader(object):
    def __init__(self, dst_directory):
        self.dst_directory = dst_directory
        self.base_url = 'http://ratedata.gaincapital.com/'
        self.downloaded_data = set()
        self.detect_downloaded_data()

    def detect_downloaded_data(self):
        for forex_pair_dir in os.listdir(self.dst_directory):
            for year_dir in os.listdir('{}/{}'.format(self.dst_directory, forex_pair_dir)):
                for month_dir in os.listdir('{}/{}/{}'.format(self.dst_directory, forex_pair_dir, year_dir)):
                    self.downloaded_data.add((forex_pair_dir, year_dir, month_dir))

    def download_data(self, years, forex_pairs):
        for year in years:
            print year
            for idx,month in enumerate(months):
                for forex_pair in forex_pairs:
                    if (forex_pair, year, month) in self.downloaded_data:
                        print 'Already Downloaded'
                        continue
                    self.downloaded_data.add((forex_pair, year, month))
                    for i in range(1,6):
                        url = self.base_url + '{}/{}%20{}/{}_Week{}.zip'.format(year, leading_zeros_string(idx+1,2), month, forex_pair, i)
                        print 'Downloading {} ...'.format(url)
                        download(url, 'Week_{}.zip'.format(i), dst_directory = '{}/{}/{}/{}'.format(self.dst_directory, forex_pair, year, month))
                        print 'Done!'

    def extract_month_csv_files(self):
        for forex_pair, year, month in self.downloaded_data:
            zip_filenames = ['{}/{}/{}/{}/Week_{}.zip'.format(self.dst_directory, forex_pair, year, month, i) for i in range(1,6)]
            csv_directory = '{}/{}/{}'.format(self.dst_directory, forex_pair, year)
            csv_filename = '{}.csv'.format(month)
            extract_and_merge(zip_filenames, '{}/{}'.format(csv_directory, csv_filename))

