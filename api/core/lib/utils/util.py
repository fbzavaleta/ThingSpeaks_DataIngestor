import requests
import pandas as pd

field_for_df = ["created_at", "entry_id", "field1", "field2", "field3", "field4", "field5", "field6", "field7", "field8"]

class TksRequest():
    def __init__(self, channelid:int):
        self.channelid = channelid

    def get_raw_data(self, n_rows:int):
        response = requests.get( self.__build_url(n_rows) )
        return response.json()["feeds"]

    def get_dataframe(sellf, n_rows):
        feed_data = self.get_raw_data(n_rows)
        return pd.DataFrame(data=feed_data, columns=field_for_df)
    
    def __build_url(self, n_rows:int):
        return f"https://api.thingspeak.com/channels/{self.channelid}/feeds.json?results={n_rows}"