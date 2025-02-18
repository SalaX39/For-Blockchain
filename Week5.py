import hashlib
import time
import random


class Block:
    def __init__(self, index, previous_hash, transactions, difficulty, miner_address):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty = difficulty
        self.miner_address = miner_address
        self.nonce = 0
        self.timestamp = time.time()
        self.hash = self.mine_block()

    def compute_hash(self):
        block_content = f"{self.index}{self.previous_hash}{self.transactions}{self.nonce}{self.miner_address}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self):
        while True:
            self.nonce += 1
            block_hash = self.compute_hash()
            if block_hash[:self.difficulty] == '0' * self.difficulty:
                return block_hash


class Blockchain:
    def __init__(self, difficulty=4, reward=50):
        self.chain = []
        self.difficulty = difficulty
        self.reward = reward
        self.pending_transactions = []
        self.miners_rewards = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], self.difficulty, "Genesis")
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            return "No transactions to mine"

        new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions, self.difficulty,
                          miner_address)
        self.chain.append(new_block)

        # Reward the miner
        self.miners_rewards[miner_address] = self.miners_rewards.get(miner_address, 0) + self.reward

        self.pending_transactions = []
        return new_block.hash

    def resolve_conflicts(self, other_chain):
        if len(other_chain) > len(self.chain):
            self.chain = other_chain
            return True
        return False


# Simulation
blockchain = Blockchain()
blockchain.add_transaction("Alice pays Bob 10 coins")

miner1 = "Miner1"
miner2 = "Miner2"

# Simulate mining competition
if random.choice([True, False]):
    print(f"{miner1} won the block")
    blockchain.mine_pending_transactions(miner1)
else:
    print(f"{miner2} won the block")
    blockchain.mine_pending_transactions(miner2)

print("Blockchain state:", [block.hash for block in blockchain.chain])
print("Miners' Rewards:", blockchain.miners_rewards)
