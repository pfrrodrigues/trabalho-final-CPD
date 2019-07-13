import csv
from trie import Trie

''' arquivo que guardara a tabela hash utilizada no projeto '''

class ElemHash():
	def __init__(self):
		self.movieid = 0
		self.generos = None
		self.raiting = 0.0
		self.num_aval  = 0
		self.filme = None
		
# calcula a hash de acordo com o movieid do usuario
def hashing_function(size_hash_table,chave, i):
	x = int(chave)
	x = (x + (i ** 2 )) % size_hash_table
	return x


# procura um filme na hash e caso encontre devolve o ElemHash
def sch_hash(hash_table, chave):
	i = 0
	slot = hashing_function(len(hash_table), chave, i)

	# verifica se slot e menor que hash e se esta ocupado
	while slot < len(hash_table) and hash_table[slot] != None:
		if hash_table[slot].movieid == chave:
			return hash_table[slot]
		i+=1
		slot = hashing_function(len(hash_table), chave, i)

	if slot >= len(hash_table):
		slot = 0
		while hash_table[slot] != None:
			if hash_table[slot].movieid == chave:
				return hash_table[slot]
			slot += 1



# procura filme na hash e adiciona o rating ao filme e incrementa o numero de avaliacoes
def search_hash(hash_table, chave, movie_raiting):
	i = 0
	slot = hashing_function(len(hash_table), chave, i)
	
	while slot < len(hash_table) and hash_table[slot] != None:

		# se o filme da hash calculada e igual a chave, add rating 
		if hash_table[slot].movieid == chave:
			hash_table[slot].num_aval += 1
			hash_table[slot].raiting = hash_table[slot].raiting + movie_raiting
			return
		# caso nao seja, incrementa i e calcula hash novamente 
		i += 1
		slot = hashing_function(len(hash_table), chave, i)
 	
 	
	if slot >= len(hash_table):
		slot = 0
		while hash_table[slot] != None:
			if hash_table[slot].movieid == chave:
				hash_table[slot].num_aval += 1
				hash_table[slot].raiting = hash_table[slot].raiting + movie_raiting
				return
			slot += 1
			

# insere um elemento na hash 
def hashing(hash_table, chave, lista_generos, titulo):
	i = 0
	slot = hashing_function(len(hash_table), chave, i)
	
	while slot < len(hash_table) and hash_table[slot] != None:
		i += 1
		slot = hashing_function(len(hash_table), chave, i)
	
	if slot >= len(hash_table):
		slot = 0
		while hash_table[slot] != None:
			slot += 1
			
	# cria um novo elemento na hash
	membro_hash = ElemHash()
	membro_hash.movieid = chave
	membro_hash.generos = lista_generos
	membro_hash.filme = titulo
	hash_table[slot] = membro_hash
