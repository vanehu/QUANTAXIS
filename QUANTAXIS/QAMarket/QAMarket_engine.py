# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market
import datetime
import random

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info


def market_stock_day_engine(__bid, client):
    coll = client.quantaxis.stock_day
    print(__bid)
    try:
        item = coll.find_one(
            {"code": str(__bid['code'])[0:6], "date": str(__bid['date'])[0:10]})
        if __bid['price'] == 'market_price':
            input()
            __bid_t = __bid
            __bid_t['price'] = (float(item["high"]) +
                                float(item["low"])) * 0.5
            return market_stock_day_engine(__bid_t, client)
        elif (float(__bid['price']) < float(item["high"]) and
                float(__bid['price']) > float(item["low"]) or
                float(__bid['price']) == float(item["low"]) or
                float(__bid['price']) == float(item['high'])) and \
                float(__bid['amount']) < float(item['volume']) / 8:
            #QA_util_log_info("deal success")
            message = {
                'header': {
                    'source': 'market',
                    'status': 200,
                    'code': str(__bid['code']),
                    'session': {
                        'user': str(__bid['user']),
                        'strategy': str(__bid['strategy'])
                    },
                    'order_id': str(__bid['order_id']),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': str(__bid['price']),
                        'code': str(__bid['code']),
                        'amount': int(__bid['amount']),
                        'date': str(__bid['date']),
                        'towards': __bid['towards']
                    },
                    'market': {
                        'open': item['open'],
                        'high': item['high'],
                        'low': item['low'],
                        'close': item['close'],
                        'volume': item['volume'],
                        'code': item['code']
                    },
                    'fee': {
                        'commission': 0.002 * float(__bid['price']) * float(__bid['amount'])
                    }
                }
            }

            # QA_signal_send(message,client)
        # print(message['body']['__bid']['amount'])
            return message
        else:
            # QA_util_log_info('not success')
            if int(__bid['price']) == 0:
                __status_mes = 401
            else:
                __status_mes = 402

            message = {
                'header': {
                    'source': 'market',
                    'status': __status_mes,
                    'code': str(__bid['code']),
                    'session': {
                        'user': str(__bid['user']),
                        'strategy': str(__bid['strategy'])
                    },
                    'order_id': str(__bid['order_id']),
                    'trade_id': str(random.random())
                },
                'body': {
                    'bid': {
                        'price': '',
                        'code': str(__bid['code']),
                        'amount': int(__bid['amount']),
                        'date': str(__bid['date']),
                        'towards': __bid['towards']
                    },
                    'market': {
                        'open': item['open'],
                        'high': item['high'],
                        'low': item['low'],
                        'close': item['close'],
                        'volume': item['volume'],
                        'code': item['code']
                    }
                }
            }
        # print(message['body']['__bid']['amount'])
            return message
    except:
        ##QA_util_log_info('no market data')
        message = {
            'header': {
                'source': 'market',
                'status': 500,
                'code': str(__bid['code']),
                'session': {
                    'user': str(__bid['user']),
                    'strategy': str(__bid['strategy'])
                },
                'order_id': str(__bid['order_id']),
                'trade_id': str(random.random())
            },
            'body': {
                '__bid': {
                    'price': str(__bid['price']),
                    'code': str(__bid['code']),
                    'amount': int(__bid['amount']),
                    'date': str(__bid['date']),
                    'towards': __bid['towards']
                },
                'market': {
                    'open': 0,
                    'high': 0,
                    'low': 0,
                    'close': 0,
                    'volume': 0,
                    'code': 0
                }
            }
        }
        return message


def market_stock_min_engine(__bid, client):
    """
    time-delay stock trading engine
    """
    pass

def market_future_day_engine(__bid,client):
    """
    future market daily trading engine
    """

    pass

def market_future_min_engine(__bid,client):
    pass
def market_future_tick_engine(__bid,client):
    pass