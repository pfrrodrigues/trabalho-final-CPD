
"""Estrutura utilizada na hash de tags """
import csv
import re

class Tag():
	
	
	def __init__(self, tag):
		self.tag = tag
		self.tag_ocupied = False
		self.taged_movies = []


def find_tag(hash_table, tag):
	for e in hash_table:
		if e != None:
			if e.tag == tag:
				return e.taged_movies


# calcula hash da tag 
def djb2(hash_size, tag):
	hash = 5381
	for c in tag:
		hash = ((hash << 5)+hash) + ord(c)
	if hash > hash_size:
		hash = hash % hash_size
	return int(hash)
	

# insere tag na hash de tags 
def hashing(hash_table,tag, mvid):
	passo = 0
	
	# calcula hash conforme a tag 
	i = djb2(len(hash_table), tag)
	base = i
	
	while hash_table[i] != None:
		# verifica se tag e igual a tag no slot
		# se for, verifica se filme ja esta na lista de tags
		# se estiver apenas retorna
		if hash_table[i].tag == tag:
			for m in hash_table[i].taged_movies:
				if m == mvid:
					return
			# senao add filme a lista da tag
			hash_table[i].taged_movies.append(mvid)
			return
		else: #  caso seja diferente calcula hash para encontrar tag novamente, caso exista
			passo += 1
			i = (base + passo*passo) % len(hash_table)
			
			if i > len(hash_table):
				i = i % len(hash_table)
				
	# caso indice esteja vazio, adiciona a nova tag
	new = Tag(tag)
	new.tag_ocupied = True
	new.taged_movies.append(mvid)
	hash_table[i] = new


