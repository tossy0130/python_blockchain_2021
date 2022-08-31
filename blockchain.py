import hashlib
import json
import logging
import sys
import time

import utils

### マイニング　ディフィカルティ
MINING_DIFFICULTY = 3
### ブロックチェーン送りて
MINING_SENDER = 'THE BLOCKCHAIN'
### 報酬の仮想通貨
MINING_REWARD = 1.0


# ログのレベルを決める ,　コンソール上にもログを表示
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

### === ブロックチェーンクラス
class BlockChain(object):
    
    def __init__(self, blockchain_address=None):
        self.transaction_pool = []  # トランザクション格納 pool
        self.chain = [] # ブロックチェーンが入るリスト
        ### 初期　（1番初めのブロック）を作成
        self.create_block(0, self.hash({}))
        ### ブロックチェーンアドレス
        self.blockchain_address = blockchain_address
        
    # ブロックを作るメソッド
    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp' : time.time(), # time スタンプ
            'transactions': self.transaction_pool, # transaction_pool
            'nonce' : nonce,
            'previous_hash' : previous_hash
        })
        ### chain に、 block を追加1
        self.chain.append(block) 
        self.transaction_pool = [] # transaction_pool を空にする
        return block
    
    ### ハッシュ 、ソート付き
    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()
    
    ### トランザクション追加 （引数）送りてのブロックチェーンアドレス => sender_blockchain_address
    ### recipient_blockchain_address => 受信
    def add_transaction(self, sender_blockchain_address, 
                        recipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address':sender_blockchain_address,
            'recipient_blockchain_address' :recipient_blockchain_address,
            'value' : float(value)
        })
        ### pool　に　トランザクション追加
        self.transaction_pool.append(transaction)
        return True
    
    def valid_proof(self, transactions, previous_hash, nonce, 
                    difficulty = MINING_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash':previous_hash
        })
        guess_block = self.hash(guess_block)
        ### 先頭文字が 000 になったら下の    proof_of_work 内の while　を止める
        return guess_block[:difficulty] == '0' * difficulty
    
    ### 
    def proof_of_work(self):
        ### トランザクション　コピー
        transactions = self.transaction_pool.copy()
        ### 最後のチェインのハッシュをもってくる
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        ### 頭に 000 がつくまで回す
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce
    
    ### マイニングメソッド
    def mining(self):
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            # ブロックチェーンアドレスを受け取る
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWARD)
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({'action': 'mining', 'status': 'sucucces'})
        return True
    
    ###################### トランザクション　の合計を計算する
    ### 引数数にアドレスを渡して計算する
    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        ### ひとつずつ ブロックを取ってくる
        for block in self.chain:
            ### トランザクションを取ってくる
            for transaction in block['transactions']:
                value = float(transaction['value'])
                ### インクリメント処理　受け取る
                if blockchain_address == transaction['recipient_blockchain_address']:
                    total_amount += value
                ### ディクリメント処理　送る
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amount -= value
        return total_amount

###### 実行 ######
if __name__ == '__main__':
    # ブロックチェーンアドレス
    my_blockchain_address = 'my_blockchain_address'
    block_chain = BlockChain(blockchain_address=my_blockchain_address) 
    utils.pprint(block_chain.chain)
    
    block_chain.add_transaction('A', 'B', 1.0)
    ### マイニング
    block_chain.mining()
    
    """"
    previous_hash = block_chain.hash(block_chain.chain[-1]) # ブロックの最後を取得
    nonce = block_chain.proof_of_work() # 
    block_chain.create_block(nonce, previous_hash) # ブロック生成
    """
    utils.pprint(block_chain.chain)
    
    block_chain.add_transaction('C', 'D', 2.0)
    block_chain.add_transaction('x', 'y', 3.0)
    ### マイニング
    block_chain.mining()
    """
    previous_hash = block_chain.hash(block_chain.chain[-1]) # ブロックの最後を取得
    nonce = block_chain.proof_of_work() # 
    block_chain.create_block(nonce, previous_hash) # ブロック生成
    """
    utils.pprint(block_chain.chain)

    
    ### 合計を求める function
    print('total' , block_chain.calculate_total_amount(my_blockchain_address))
    print('C' , block_chain.calculate_total_amount('C'))
    print('D' , block_chain.calculate_total_amount('D'))