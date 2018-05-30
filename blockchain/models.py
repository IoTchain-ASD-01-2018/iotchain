# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import hashlib as hasher
import json
import os
from datetime import datetime

from cryptography.fernet import Fernet, InvalidToken

def get_endereco_blockchain():
    """Lê o arquivo onde está a blockchain"""
    # pega o path absoluto do script
    path_atual = os.path.dirname(__file__) 
    # concatena o path absoluto com o relativo
    return os.path.join(path_atual, "blockchain.json")


class Block:
    def __init__(self, index, data_insercao, dados, hash_anterior):
        """Construtor da classe"""
        self.index = index
        self.data_insercao = data_insercao
        self.dados = dados
        self.hash_anterior = hash_anterior
        self.hash = self.hash_block()

    def hash_block(self):
        """Cria um hash para o bloco"""
        sha = hasher.sha256((str(self.index) + 
                str(self.data_insercao) + 
                str(self.dados) +
                str(self.hash_anterior)).encode('utf-8'))
        return sha.hexdigest()

    def criar_json_do_bloco(self):
        """Cria um objeto python para o bloco"""
        json_block = {
            "index": self.index,
            "data_insercao": self.data_insercao.strftime("%Y-%m-%d %H:%M:%S"),
            "dados": self.dados,
            "hash_anterior": self.hash_anterior,
            "hash": self.hash
        }
        return json_block

    def inserir_bloco_na_blockchain(self):
        """Persiste o bloco na blockchain"""
        json_block = self.criar_json_do_bloco()
        blockchain = ler_blockchain()
        blockchain['blocks'].append(json_block)
        path_blockchain = get_endereco_blockchain()
        with open(path_blockchain, 'w') as arquivo:
            json.dump(blockchain, arquivo)


def ler_arquivo():
    """Interpreta o arquivo que contém a blockchain"""
    path_blockchain = get_endereco_blockchain()
    with open(path_blockchain, 'r') as arquivo:
        blockchain = json.load(arquivo)
    return blockchain

def get_ultimo_bloco():
    """Retorna o último bloco em um JSON"""
    blockchain = ler_arquivo()
    maior_index = -1
    ultimo_bloco = {}
    for bloco in blockchain['blocks']:
        if bloco['index'] > maior_index:
            maior_index = bloco['index']
            ultimo_bloco = bloco
    return ultimo_bloco


def ler_chave():
    path = os.path.dirname(__file__)
    with open("{}/chave.txt".format(path), "r") as arquivo:
        chave = arquivo.read()
    return chave


def criptografar(conteudo):
    crip = Fernet(str(ler_chave()))
    return crip.encrypt(str(conteudo))


def descriptografar(conteudo):
    chave = ler_chave()
    crip = Fernet(chave)
    try:
        return crip.decrypt(bytes(conteudo))
    except InvalidToken:
        return ""


def proximo_bloco(ultimo_bloco, novos_dados):
    """Cria um novo bloco a partir do último da blockchain"""
    index = ultimo_bloco['index'] + 1
    data_insercao = datetime.now()
    dados = novos_dados
    dados['origem'] = criptografar(bytes(dados['origem']))
    dados['destino'] = criptografar(bytes(dados['destino']))
    hash_anterior = ultimo_bloco['hash']
    return Block(index, data_insercao, dados, hash_anterior)

def ler_blockchain(index=None, hash_bloco=None, origem=None, destino=None):
    """Retorna um bloco se especificado seu index ou hash.
    Caso contrário, retorna todo o bloco"""
    blockchain = ler_arquivo()
    if index is not None:
        for bloco in blockchain['blocks']:
            if bloco['index'] == int(index):
                return bloco
    if hash_bloco is not None:
        for bloco in blockchain['blocks']:
            if bloco['hash'] == hash_bloco:
                return bloco
    if origem is not None:
        for bloco in blockchain['blocks']:
            descriptografado = descriptografar(bloco['dados']['origem'])
            print(descriptografado)
            print(origem)
            if descriptografado == origem:
                bloco['dados']['origem'] = descriptografado
                return bloco
    if destino is not None:
        for bloco in blockchain['blocks']:
            descriptografado = descriptografar(bloco['dados']['destino'])
            if descriptografado == destino:
                bloco['dados']['destino'] = descriptografado
                return bloco
    return blockchain
                
