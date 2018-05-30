# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import JSONEncoder, loads

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import Block, ler_blockchain, proximo_bloco, get_ultimo_bloco

def responder(dict_obj, status):
    return HttpResponse(JSONEncoder().encode(dict_obj),
                        200)


def request_blockchain(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        ultimo_bloco = get_ultimo_bloco()

        novo_bloco = proximo_bloco(ultimo_bloco, body)
        novo_bloco.inserir_bloco_na_blockchain()

        return responder(novo_bloco.criar_json_do_bloco(), 200)

    if request.method == 'GET':
        query_string = request.GET.urlencode()
        dados = {
            "index": None,
            "hash": None,
            "origem": None,
            "destino": None
        }
        if len(query_string) > 0:
            query_string = query_string.split("&")
            for query in query_string:
                query = query.split("=")
                dados[query[0]] = query[1]
        return responder(ler_blockchain(dados['index'],
                                        dados['hash'],
                                        dados['origem'],
                                        dados['destino']),
                         200)
