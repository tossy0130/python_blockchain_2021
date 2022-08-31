import hashlib
import collections



### key　で ソート
def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(),key=lambda d:[0]))


### 出力関数 ###
def pprint(chains):
    for i , chain in enumerate(chains):
        print(f'{"=" * 25} Chain {i} {"=" * 25}')
        for k, v in chain.items():
            
            if k == 'transactions':
                print(k)
                for d in v:
                    print(f'{"-" * 40}')
                    for kk, vv in d.items():
                        print(f' {kk:30}{vv}')
            else:    
                print(f'{k:15}{v}')
    print(f'{"*" * 25}')
        