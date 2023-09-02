#!/usr/bin/python
# Usage - brute4brute.py -Q quantidade -T threads -U url 2023-09-01 23:45:55$
# Author: Knz-Source
# Copyright: No intelectual property
import argparse
import random
import string
import requests
import threading

def generate_random_id():
    id_parts = []
    for _ in range(3):
        id_part = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        id_parts.append(id_part)
    return '.'.join(id_parts)

def check_id_validity(url, id):
    full_url = url + id
    response = requests.get(full_url)
    if response.status_code == 200:
        return response.text  # Retorna o conteúdo da página
    else:
        return None  # Retorna None se a solicitação falhar

def worker(thread_id, url, quantity):
    for _ in range(quantity):
        id = generate_random_id()
        response_content = check_id_validity(url, id)
        if response_content is not None:
            print(f"Thread-{thread_id}: ID: {id} - Válido - Conteúdo da Página: {response_content}")
        else:
            print(f"Thread-{thread_id}: ID: {id} - Inválido")

def main():
    parser = argparse.ArgumentParser(description="Gerador de IDs e envio de solicitações para uma URL")
    parser.add_argument("-Q", "--quantity", type=int, help="Quantidade de IDs a serem gerados por thread", required=True)
    parser.add_argument("-U", "--url", type=str, help="URL para enviar as solicitações", required=True)
    parser.add_argument("-T", "--threads", type=int, help="Número de threads a serem usadas", required=True)
    args = parser.parse_args()

    threads = []
    for i in range(args.threads):
        thread = threading.Thread(target=worker, args=(i, args.url, args.quantity))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

