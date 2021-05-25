from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

import os
import environ
from pathlib import Path
from requests_oauthlib import OAuth1Session
import json

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


class IndexView(TemplateView):
    """トップページ"""
    template_name = 'we_bought_again/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        API_Key = env('API_Key')
        API_Secret_Key = env('API_Secret_Key')
        Access_Token = env('Access_Token')
        Access_Token_Secret = env('Access_Token_Secret')

        data_list = []
        # context = {}
        cnt = 0

        twitter = OAuth1Session(API_Key, API_Secret_Key, Access_Token, Access_Token_Secret)
        search_api = 'https://api.twitter.com/1.1/search/tweets.json'
        oembed_api = 'https://publish.twitter.com/oembed'

        params = {
            # 波ダッシュ、全角チルダ
            'q': '#はぁ〜また買っちゃった OR #はぁ～また買っちゃった -filter:retweets',
            'result_type': 'recent',
            'count': 30,
        }

        print('get res...')
        res = twitter.get(search_api, params=params)
        tweets = json.loads(res.text)

        print('embed...')
        for row in tweets['statuses']:
            cnt += 1
            print(cnt, end='\t')
            try:
                is_media = row['entities']['media']
                name = row['user']['name']
                screen_name = row['user']['screen_name']
                id = row['id']

                oembed_url = f'https://twitter.com/{screen_name}/status/{id}'
                oembed_params = {
                    'url': oembed_url,
                    'align': 'center',
                    'hide_thread': 'true',
                }
                print(screen_name)
                request = twitter.get(oembed_api, params=oembed_params)
                e_data = json.loads(request.text)['html']
                data_list.append(e_data)
                context['e_data'] = data_list
            except KeyError:
                print('pass')
                continue

        return context
