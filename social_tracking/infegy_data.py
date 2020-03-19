from atlas_api import atlas_request
import pandas as pd
import requests, json
from datetime import datetime, date
from wordcloud import WordCloud
import  matplotlib.pyplot as plt


class Infegy:

    keyword = "coronavirus OR corona virus OR covid-19 OR covid 19"

    def run(self, api_key, endpoint, choice):

        query_jan11 = 'https://atlas.infegy.com/api/v2/' + endpoint + '.json?query_builder_detail=%7B%22or_items%22%3A%5B%7B%22type%22%3A%22text%22%2C%22value%22%3A%22%5C%22corona%20virus%5C%22%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22covid-19%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22coronavirus%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22%5C%22covid%2019%5C%22%22%7D%5D%7D&start_date=2020-01-11&end_date=Now&category=twitter%2Cfacebook%2Cinstagram%2Cpinterest&limit=200&api_key=' + api_key
        query = 'https://atlas.infegy.com/api/v2/' + endpoint + '.json?query_builder_detail=%7B%22or_items%22%3A%5B%7B%22type%22%3A%22text%22%2C%22value%22%3A%22%5C%22corona%20virus%5C%22%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22covid-19%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22coronavirus%22%7D%2C%7B%22type%22%3A%22text%22%2C%22value%22%3A%22%5C%22covid%2019%5C%22%22%7D%5D%7D&start_date=2%20days%20ago&end_date=Now&category=twitter%2Cfacebook%2Cinstagram%2Cpinterest&limit=200&api_key=' +  api_key

        if choice == 'jan 11':
            jan11_response = requests.get(url = query_jan11)
            jan11_response = json.loads(jan11_response.text)
            return jan11_response
        elif choice == 'two days':
            query_response = requests.get(url = query)
            query_response = json.loads(query_response.text)
            return query_response
        else: print('Please enter jan 11 or two days')

    #volume
    def volume(self):

        response = self.run(endpoint= 'volume', choice = 'jan 11')
        date_list = [response['output'][x]['date'] for x in range(len(response['output']))]
        count_list = [response['output'][x]['posts_normalized_universe'] for x in range(len(response['output']))]

        volume_trend = pd.DataFrame(data={'date': date_list, 'posts_normalized': count_list})
        volume_trend['date'] = pd.to_datetime(volume_trend['date'], utc=True).apply(lambda x: x.date())

        return volume_trend


    #state
    def state(self):

        response = self.run(endpoint = 'states', choice = 'two days')

        code_list = [response['output'][x]['code'] for x in range(len(response['output']))]
        name_list = [response['output'][x]['name'] for x in range(len(response['output']))]
        score_list = [response['output'][x]['score'] for x in range(len(response['output']))]

        df = pd.DataFrame({'Name': name_list, 'Score': score_list})
        df = df.sort_values(by = 'Score', ascending= False)
        df['Ranking'] = range(1, len(df)+1)
        df = df[['Ranking','Name','Score']]

        return df

    #dma
    def dma(self):
        response = self.run(endpoint='dma', choice = 'two days')

        name_list = [response['output'][x]['name'] for x in range(len(response['output']))]
        post_list = [response['output'][x]['matches'] for x in range(len(response['output']))]

        df = pd.DataFrame({'DMA_name': name_list, 'Posts_Count': post_list})
        df = df.sort_values(by='Posts_Count', ascending=False)
        df['Ranking'] = range(1, len(df) + 1)
        df = df[['Ranking', 'DMA_name', 'Posts_Count']]

        return df

    #entities - company

    def entity_wordcoud(self):
        response = self.run(endpoint = 'entities', choice = 'two days')

        name_list = [response['output'][x]['name'] for x in range(len(response['output'])) if response['output'][x]['entity_type'] == 'company']
        frequency = [response['output'][x]['appearances'] for x in range(len(response['output'])) if response['output'][x]['entity_type'] == 'company']

        freq_dict = dict(zip(name_list, frequency))

        w1 = WordCloud(width=1600, height=800, background_color='white', colormap='Blues', margin=1,min_word_length=0).generate_from_frequencies(
            freq_dict)
        entity_fig = plt.figure(figsize=(20, 10))
        plt.imshow(w1, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('entity_wc.png')
        plt.close(entity_fig)
        return  entity_fig

    def entity_table(self):

        response = self.run(endpoint='entities', choice='two days')

        name_list = [response['output'][x]['name'] for x in range(len(response['output']))]
        frequency = [response['output'][x]['appearances'] for x in range(len(response['output']))]

        df = pd.DataFrame({'Entity': name_list, 'Frequency': frequency})
        df = df.sort_values(by = 'Frequency', ascending=False).head(10)
        df['Ranking'] = range(1,len(df)+1)
        df = df[['Ranking', 'Entity']]

        return df

