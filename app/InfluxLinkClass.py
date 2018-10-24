#!/user/bin/python3.5
import json
import requests

header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}

import pandas as pd
from influxdb import InfluxDBClient, DataFrameClient



class Influx_our():

    def __init__(self, host, port, user, password, db_name, query_body, json_body_to_write):

        self.host = host

        self.port = port

        self.user = user

        self.password = password

        self.db_name = db_name

        self.query_body = query_body

        self.json_body_to_write = json_body_to_write

        self.client = InfluxDBClient(self.host, self.port, self.user, self.password, self.db_name)

    def get_data_as_list(self):

        self.rs_tag = self.client.query(self.query_body)

        self.data = list(self.rs_tag.get_points())

        return self.data

    def convert_to_df_second(self, data):
        main_d = dict()
        for i in range(len(data)):
            main_d[list(data[i].values())[1]] = list(data[i].values())[0]
        data1 = pd.Series(main_d)
        print(data1)
        df = data1.to_frame()
        df = df.reset_index()
        df.columns = ['date', 'value']
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        return self.df


    def convert_to_df_first(self, data):
        main_d = dict()
        for i in range(len(data)):
            main_d[list(data[i].values())[0]] = list(data[i].values())[1]
        data1 = pd.Series(main_d)
        print(data1)
        df = data1.to_frame()
        df = df.reset_index()
        df.columns = ['date', 'value']
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        return self.df


    def get_data_as_df(self):

        data_to_df = self.get_data_as_list()

        if list(data_to_df[0].keys())[1] == "time":
            df_tag = self.convert_to_df_second(data_to_df)
        else:
            df_tag = self.convert_to_df_first(data_to_df)

        self.current_time = pd.to_datetime(df_tag.index.values[-1])

        return df_tag

    def read_data(self):

        return self.get_data_as_df()


    def write_data_to_influx(self):

        self.client.write_points(self.json_body_to_write)

