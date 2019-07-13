# Trabalho Final da Disciplina Classificacao e Pesquisa de Dados
# Aluno: Pablo Rodrigues 
# Aluno: Hirwin Nunes
# ATENCAO: COLOCAR ARQUIVOS NA PASTA

import csv
import sys
import re
import hashh
import tag
import console
from trie import Trie


# definicacao das estruturas
hash_table = [None for x in range(45000)]
special_list = [([],[]) for valor in range(0, 138494)]		 # lista ordenada que guardara usuarios e rating/filmes
hash_tag = [None for x in range(40000)]					

# nomeacao dos arquivos 
filename = 'movie.csv'
filerat = 'minirating.csv'
tagfile = 'tag.csv'

root = Trie() # cria raiz da arvore Trie 
Trie.root = root

""" Inicio da remocao de dados """

print("Montando Trie e Hash...")
with open(filename, encoding="utf-8") as f:
	reader = csv.reader(f, delimiter=',', skipinitialspace=True)
	linha = next(reader)					
	for line in reader:
		""" Montagem da Hash e da Trie """ 
		hashh.hashing(hash_table, int(line[0]), line[2], line[1])							 
		root.insere((re.sub('[^A-Za-z0-9]+', '', line[1])).upper(), int(line[0]), line[1])		
print("Fim da montagem da Trie e Hash.")


print("\nMontando Estrutura Especial...")
with open(filerat, encoding="utf-8") as file_object:
	rea = csv.reader(file_object, delimiter=',', skipinitialspace=True)
	linha = next(rea)

	for line in rea:
		# usa id do usuario como indice 
		# e insere na tupla de listas ([movieid],[rating do filme])
		special_list[int(line[0])][0].append(int(line[1]))
		special_list[int(line[0])][1].append(float(line[2]))
		
		# procura filme na hash e adiciona rating ao filme
		hashh.search_hash(hash_table,int(line[1]), float(line[2]))
print("Fim da montagem da Estrutura Especial.\n")


print("Montando Hash de Tags...")
with open(tagfile, encoding="utf-8") as csvtag:
	tagreader = csv.reader(csvtag, delimiter=',', skipinitialspace=True)
	header = next(tagreader)

	for row in tagreader:
		# insere nova tag na hash e add filme na sua lista de filmes com a tag se filme ainda nao foi tageado
		tag.hashing(hash_tag, (re.sub('[^A-Za-z0-9]+', '', row[2])).upper(), int(row[1]))
print("Fim da montagem da Hash de Tags.")

# cria uma lista ordenada pelo numero de avaliacoes
ordered = hash_table[:]
ordered = [value for value in ordered if value != None]
ordered.sort(key=lambda data: data.num_aval, reverse=True)		

print("REMOCAO DE DADOS COMPLETA.")

# Entra no modo de console 
console.menu(hash_table, special_list, ordered, hash_tag)
