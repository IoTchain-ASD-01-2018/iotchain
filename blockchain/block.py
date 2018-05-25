# Fonte: https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b

import hashlib as hasher

class Block:
  def __init__(self, index, data_insercao, dados, hash_anterior):
    self.index = index
    self.data_insercao = data_insercao
    self.dados = dados
    self.hash_anterior = hash_anterior
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + 
               str(self.data_insercao) + 
               str(self.dados) + 
               str(self.hash_anterior))
    return sha.hexdigest()
