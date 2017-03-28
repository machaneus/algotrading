import pandas as pd

class SecurityBlock(object):

    def __init__(self, grouping_interval='1Min', grouping_method='ohlc', date_parse = None):
        if date_parse == None:
            self.date_parse = lambda x: pd.datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S')
        else:
            self.date_parse = date_parse

        self.grouping_interval = grouping_interval
        self.grouping_method = grouping_method
        self.df_dict = dict()

    def add_csv(self, csv_filename, forex_pair_name, column_names, date_time_name, column_names_to_delete):
        dataframe_resampled = self.load_csv(csv_filename, column_names, date_time_name, column_names_to_delete).resample(self.grouping_interval, how=self.grouping_method)
        if forex_pair not in self.df_dict.keys():
            self.df_dict[forex_pair] = dataframe_resampled
        else:
            self.df_dict[forex_pair] = pd.concat([self.df_dict[forex_pair], dataframe_resampled])


    def load_csv(self, csv_filename, names, date_time_name, names_to_delete):

        dataframe = pd.read_csv(csv_filename, skiprows=[0], parse_dates=[date_time_name], index_col=date_time_name, names=names, date_parser=self.date_parse)

        for name in names_to_delete:
            del dataframe[name]

        return dataframe

    def save(self):
		for (key, value) in self.df_dict:
        	value.to_pickle('*TODO*')

    
