import json
import requests

API_URL = 'http://localhost:8000/api/'

class Experiment:
    def __init__(self,
                 name,
                 description='',
                 parameters=None,
                 outcome=None,
                 access_token=None,
                 likelihood='GAUSSIAN'): # other option is NOISELESS
        self.name = name
        self.parameters = parameters
        self.outcome = outcome
        api_params = {'name': name}
        r = requests.get(API_URL + 'find_experiment', params=api_params).json()
        if (r['result']): # found experiment
            print 'resuming experiment ' + name + '...'
        else:
            api_params['parameters'] = parameters
            api_params['outcome'] = outcome
            r = requests.post(API_URL + 'create_experiment/', data=json.dumps(api_params)).json()
            if 'error' in r:
                raise RuntimeError('failed to create experiment ' + name + '. error: ' + r['error'])
            else:
                print 'experiment ' + name + ' was created.'

    def suggest(self):
        api_params = {'name': self.name}
        r = requests.get(API_URL + 'get_suggestion', params=api_params).json()
        if 'error' in r:
            raise RuntimeError('failed to get suggestion from spearmint. error: ' + r['error'])
        else:
            return r['params']

    def update(self, param_values, outcome_val):
        api_params = {'name': self.name, 'outcome_val': outcome_val}
        r = requests.post(API_URL + 'post_update/', data=api_params).json()
        if 'error' in r:
            raise RuntimeError('failed to post update to spearmint. error: ' + r['error'])
