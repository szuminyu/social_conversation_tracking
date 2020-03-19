import requests, json
import pandas as pd
from wordcloud import WordCloud
import  matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
pd.set_option('display.max_columns', None)

'''
documentation: https://developer.newswhip.com/reference#articles

api_key = 'your key'
api_endpoint = 'https://api.newswhip.com/v1/articles?key=%s' or 'https://api.newswhip.com/v1/stats?key=%s'

'''


class Newswhip_article:

    def __init__(self, api_key, api_endpoint = 'https://api.newswhip.com/v1/articles?key=%s'):
        self.api_key = api_key
        self.api_endpoint = api_endpoint % self.api_key

    def news_response(self, time_from = int((datetime.today() - timedelta(days = 2)).timestamp() * 1000)):

        # query = corona virus OR COVID-19 OR COVID 19 or cornoavirus
        # country code: United States
        # two days ago

        data = json.dumps({'filters': ["country_code: us AND headline:(\"corona virus\" OR \"COVID-19\" OR \"COVID 19\" OR \"coronavirus\") "],
                           'from': time_from})
        news_response = requests.post(url=self.api_endpoint, data=data)
        response = json.loads(news_response.text)

        return response

    def headline_text(self):

        response = self.news_response()
        list_1 = []

        for i in range(0, response['articles'].__len__()):
            list_1.append(response['articles'][i]['headline'])

        data = pd.Series(list_1)

        # preprocessing for wordcloud
        # lower
        data = data.apply(lambda x: x.lower())
        # punctutation
        data = data.str.replace("[^a-zA-Z0-9'’]", ' ')
        # remove stopwords
        from nltk.corpus import stopwords
        stopwords = stopwords.words('english')
        data = data.apply(lambda x: ' '.join(x for x in x.split() if x not in stopwords))
        # customed stopwords
        keyword = ["corona virus", "coronavirus", "covid-19", "covid 19", "covid", "likely", "19"]
        data = data.apply(lambda x: ' '.join(x for x in x.split() if x not in keyword))


        return data

    def get_ngrams(self, input, n):
        input = input.split(' ')
        output = {}
        for i in range(len(input) - n + 1):
            g = ' '.join(input[i:i + n])
            output.setdefault(g, 0)
            output[g] += 1
        return output

    def bigram(self):
        data = self.headline_text()
        my_bigrams = self.get_ngrams(' '.join(data), 2)

        w1 = WordCloud(width=1600, height=800, background_color='white', colormap='Reds').generate_from_frequencies(
            my_bigrams)
        bigram_fig = plt.figure(figsize=(20, 10))
        plt.imshow(w1, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('bigram.png')
        plt.close(bigram_fig)
        return  bigram_fig

    def threegram(self):
        data = self.headline_text()
        three_grams = self.get_ngrams(' '.join(data), 3)

        w2 = WordCloud(width=1600, height=800, background_color='white', colormap='Oranges').generate_from_frequencies(
            three_grams)
        threegram_fig = plt.figure(figsize=(20, 10))
        plt.imshow(w2, interpolation='bilinear')
        plt.axis('off')
        plt.margins(x=0, y=0)
        plt.savefig('threegram.png')
        plt.close(threegram_fig)
        return threegram_fig


    ## engagement posts table

    def engagement_articles(self):
        response = self.news_response()

        list_1 = [response['articles'][i]['headline'] for i in range(len(response['articles']))]  #headline
        list_2 = [response['articles'][i]['source']['publisher'] for i in range(len(response['articles']))]  #source
        list_3 = [response['articles'][i]['fb_data']['total_engagement_count'] for i in range(len(response['articles']))]  #engagement on facebook
        list_4 = [response['articles'][i]['link'] for i in range(len(response['articles']))]  #link
        list_5 = [response['articles'][i]['authors'] for i in range(len(response['articles']))]  #authors
        list_5 = ['None' if v is None else v for v in list_5]

        df = pd.DataFrame({'Headline': list_1, 'Source': list_2, 'Facebook Interaction': list_3, 'Link': list_4, 'Author': list_5})
        df['Author'] = df['Author'].apply(lambda x: ' '.join(items for items in x))
        df = df.sort_values(by = 'Facebook Interaction', ascending=False).head(5)
        df = df[['Headline', 'Source', 'Author', 'Facebook Interaction', 'Link']]
        return df

class Newswhip_stats:

    def __init__(self, api_key , api_endpoint = 'https://api.newswhip.com/v1/stats?key=%s'):
        self.api_key = api_key
        self.api_endpoint = api_endpoint % self.api_key

    def trend_period(self, sdate = datetime(2020, 1, 11, 12, 0)):
        timestamp_list = []
        date_list = []

        # start date: Jan 11 (for the line chart)
        edate = datetime.today()  # end date

        delta = edate - sdate  # as timedelta

        for i in range(delta.days + 1):
            date_list.append(sdate + timedelta(days=i))
            timestamp_list.append(int((sdate + timedelta(days=i)).timestamp()*1000))

        return timestamp_list, date_list

    def trend_data(self, time_from, time_to, filter_choice):
        total = 0

        if filter_choice == 'us':
            data = json.dumps({'filters': [
                "country_code: us AND headline:(\"corona virus\" OR \"COVID-19\" OR \"COVID 19\" OR \"coronavirus\") "],
                               'from': time_from,
                               'to': time_to,
                               'sort_by': 'fb_total.sum',
                               'aggregate_by': 'country_code'})
            stats_response = requests.post(url= self.api_endpoint, data=data)
            stats = json.loads(stats_response.text)
            for i in range(len(stats)):
                total += int(stats[i]['stats']['fb_total']['count'])
                total += int(stats[i]['stats']['twitter']['count'])
                total += int(stats[i]['stats']['pinterest']['count'])
                total += int(stats[i]['stats']['linkedin']['count'])
            return total

        elif filter_choice == 'global':
            data = json.dumps({'filters': ["headline:(\"corona virus\" OR \"COVID-19\" OR \"COVID 19\" OR \"coronavirus\") "],
                                'from': time_from,
                                'to': time_to,
                                'sort_by': 'fb_total.sum',
                                'aggregate_by': 'country_code'})
            stats_response = requests.post(url= self.api_endpoint, data=data)
            stats = json.loads(stats_response.text)

            for i in range(len(stats)):
                total += int(stats[i]['stats']['fb_total']['count'])
                total += int(stats[i]['stats']['twitter']['count'])
                total += int(stats[i]['stats']['pinterest']['count'])
                total += int(stats[i]['stats']['linkedin']['count'])
            return total

        elif filter_choice == 'publisher':
            data = json.dumps({'filters': ["headline:(\"corona virus\" OR \"COVID-19\" OR \"COVID 19\" OR \"coronavirus\") "],
                                'from': time_from,
                                'to': time_to,
                                'sort_by': 'fb_total.sum',
                                'aggregate_by': 'publisher'})

            stats_response = requests.post(url= self.api_endpoint, data=data)
            stats = json.loads(stats_response.text)

            return stats

        else: print('Please enter us or global or publisher.')


    def trend_df(self):
        timestamp_list, date_list = self.trend_period()
        total_count_us = []
        total_count_global = []

        for i in range(len(timestamp_list)-1):
            total_count_us.append(self.trend_data(time_from = timestamp_list[i], time_to= timestamp_list[i+1], filter_choice = 'us'))
            total_count_global.append(self.trend_data(time_from=timestamp_list[i], time_to=timestamp_list[i+1], filter_choice='global'))

        df = pd.DataFrame({'time': date_list[:-1], 'total_posts_us': total_count_us, 'total_posts_global': total_count_global})
        df['time'] = pd.to_datetime(df['time'], utc=True).apply(lambda x: x.date())

        return df


    def top_publisher(self):

        time_from = int((datetime.today() - timedelta(days=2)).timestamp() * 1000)  # 2 days ago
        time_to = int(datetime.today().timestamp() * 1000)

        stats = self.trend_data(time_from = time_from, time_to= time_to, filter_choice = 'publisher')

        publisher_list = []
        fb_total = []

        for i in range(len(stats)):
            publisher_list.append(stats[i]['key'])
            fb_total.append(int(stats[i]['stats']['fb_total']['sum']))

        df = pd.DataFrame({'Publisher': publisher_list, 'Facebook Interactions': fb_total}).sort_values(by = 'Facebook Interactions', ascending=False).head(10)

        '''
        # get interactions
        article_api_endpoint = 'https://api.newswhip.com/v1/articles?key=%s' % self.api_key

        list_sum = []
        list_avg = []

        for i in range(len(df)):
            data = json.dumps({'filters': ["headline:(\"corona virus\" OR \"COVID-19\" OR \"COVID 19\" OR \"coronavirus\") AND -publisher:" + df.iloc[i, 0]],
                                'from': time_from,
                                'to': time_to})
            article_response = requests.post(url= article_api_endpoint, data=data)
            response = json.loads(article_response.text)

            #calculate the sum and average
            num_sum = 0
            for j in range(len(response['articles'])):
                num_sum += response['articles'][i]['predicted_interactions']
            list_sum.append(int(num_sum))
            list_avg.append(int(num_sum / len(response['articles'])))

        df['Avg Predicted Interactions'] = list_avg
        df['Total Predicted Interactions'] = list_sum
        '''

        return df


