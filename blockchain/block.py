# -*- coding: utf-8 -*-
# Fonte: https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b

import hashlib as hasher
from datetime import datetime

class Block:
  def __init__(self, index, data_insercao, dados, hash_anterior):
    self.index = index
    self.data_insercao = data_insercao
    self.dados = dados
    self.hash_anterior = hash_anterior
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256((str(self.index) + 
               str(self.data_insercao) + 
               str(self.dados) +
               str(self.hash_anterior)).encode('utf-8'))
    return sha.hexdigest()


def criar_bloco_genesis():
  return Block(0, datetime.now(), {"origem": "bloco genesis", "destino": "bloco genesis"}, "0")

def proximo_bloco(ultimo_bloco, novos_dados):
  index = ultimo_bloco.index + 1
  data_insercao = datetime.now()
  dados = novos_dados
  hash_anterior = ultimo_bloco.hash
  return Block(index, data_insercao, dados, hash_anterior)

# codigo abaixo apenas para teste
blockchain = [criar_bloco_genesis()]
blockchain.append(proximo_bloco(blockchain[0], {"origem": "primeira origem", "destino": "novo destino"}))
for block in blockchain:
  print(block.hash)