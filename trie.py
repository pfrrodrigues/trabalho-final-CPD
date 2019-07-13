
''' Classe Trie '''
''' Tentativa de representar uma estrutura de dados Arvore Trie '''

class Trie():
	"""Representa a estrutura de dados Trie"""
	
	""" lista estatica que guardara os filmes pesquisados"""
	movie_list = []
	title = None
	root = None
	
	def __init__(self, movie_id=-1):
		"""Inicializa os atributos da classe"""
		self.movie_id = movie_id
		self.marcador = False
		self.filhos = [None for value in range(0,36)]
		self.letra = None
		self.movie_name = None

	"""calcula indice de insercao de um caractere"""
	def index(self, palavra):
		index = ord(palavra[0])-48
		if ord(palavra[0])-48 > 9:
			index -= 7
	
		return index

	"""Verifica se um nodo tem filhos """
	def childrens(self, childrens):
		for x in childrens:
			if x != None:
				return True
		return False

	"""Insere na lista estatica todos os filmes a partir do prefixo"""
	def all_words(self, root):

		if root.childrens(root.filhos):
			for children in root.filhos:
				if children != None:
					if children.marcador == True:
						tup = (children.movie_name, children.movie_id)
						Trie.movie_list.append(tup)
					root.all_words(children)


	"""Procura filme na trie baseado no prefixo dado"""
	def search_trie(self, word_search):

		if not word_search:
			print("PALAVRA INVALIDA.")
		
		indice = self.index(word_search)

		if len(word_search) == 1:
			if self.filhos[indice] != None:
				if self.filhos[indice].marcador == True:
					tup = (self.filhos[indice].movie_name, self.filhos[indice].movie_id)
					Trie.movie_list.append(tup)
				self.all_words(self.filhos[indice]) # coloca na lista todos os marcadores abaixo
				return
									
		if len(word_search) > 1:
			# signfica que existe o nodo e que sao iguais
			if self.filhos[indice] != None:
				self.filhos[indice].search_trie(word_search[1:])	# chamada a funcao recursiva


	"""Insere novo filme na trie """ 
	def insere(self,palavra, mv_id, original):
		#calcula o indice de insercao na lista de filhos self '''		
		indice = self.index(palavra)

		if len(palavra) > 1:
			if self.filhos[indice] == None:
				nodo = Trie()
				nodo.letra = palavra[0]
				self.filhos[indice] = nodo
			(self.filhos[indice]).insere(palavra[1:], mv_id, original)
		else:
			if self.filhos[indice] is None:
				nodo = Trie()
				nodo.letra = palavra[0]
				nodo.marcador = True
				nodo.movie_id = mv_id
				nodo.movie_name = original
				
				self.filhos.insert(indice, nodo)
			else:
				self.filhos[indice].marcador = True
				self.filhos[indice].movie_name = original
