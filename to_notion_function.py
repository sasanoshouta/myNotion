# Notionとの連携に使用
import datetime
import json
from pprint import pprint
import requests

import numpy as np
import pandas as pd
from .config import Config
from .propertytype import PropertyType

def to_notion(cells):
    props = {}
    
    for cell in cells:
        props.update(cell.to_dict())
    
    body = {
        'parent': {
            'database_id': Config.database_id
        },
        'properties': props,
    }

    url = f'{Config.notion_endpoint}/pages'
    return requests.request('POST', url=url, headers=Config.headers, data=json.dumps(body))

class Cell:
    def __init__(self, key, properties, values):
        self.key = key
        self.property_type = properties[self.key]
        self.values = values

    def to_dict(self):
        if self.property_type in [PropertyType.TITLE, PropertyType.RICH_TEXT]:
            return self._to_dict_text()
        elif self.property_type == PropertyType.DATE:
            return self._to_dict_pattern2('start')
        elif self.property_type == PropertyType.NUMBER:
            return self._to_dict_pattern1(round(self.values, 5))
        elif self.property_type == PropertyType.CHECKBOX:
            return self._to_dict_pattern1(self.values)
        elif self.property_type == PropertyType.SELECT:
            return self._to_dict_pattern2('name')
        elif self.property_type == PropertyType.MULTI_SELECT:
            values = self.get_multi_select_values()
            return self._to_dict_pattern1(values)
        elif self.property_type == PropertyType.RELATION:
            return self._to_dict_relation()

    def _to_dict_text(self):
        return {
            self.key: {
                self.property_type: [
                    {
                        'text': {
                            'content': self.values
                        }
                    }
                ]
            }
        }

    def _to_dict_relation(self):
        return {
            self.key: {
                self.property_type: [
                    {
                        'id': self.get_page_id()
                    }
                ]
            }
        }

    def _to_dict_pattern1(self, values):
        return {
            self.key: {
                self.property_type: values
            }
        }

    def _to_dict_pattern2(self, name):
        return {
            self.key: {
                self.property_type: {
                    name: self.values
                }
            }
        }

    def get_multi_select_values(self):
        values = []
        if isinstance(self.values, str):
            values.append({'name': self.values})
        else:
            for val in self.values:
                values.append({'name': val})
        return values
    
    def get_page_id(self):
        body = {
            'filter': {
                'property': 'Exp',
                'text': {
                    'contains': self.values
                }
            }
        }
        url = f'{Config.notion_endpoint}/databases/{Config.database_id}/query'
        response = requests.request('POST', url=url, headers=Config.headers, data=json.dumps(body))

        return response.json()['results'][0]['id']