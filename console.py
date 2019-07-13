import re
import hashh
from trie import Trie
from prettytable import PrettyTable
from tag import find_tag

""" Tratamento do comando 'movie' """
def movie(list_of_movies, hash_table, filme):
	
	# pesquisa prefixo na trie e armazena na lista estatica da classe a lista de filmes com o prefixo
	Trie.root.search_trie((re.sub('[^A-Za-z0-9]+', '', filme)).upper())
	# ordenada lista de prefixos pelo id 
	Trie.movie_list.sort(key=lambda tup: tup[1])
	
	t = PrettyTable(['movieid','title','genres','rating', 'count'])
	
	# procura dados de rating e numero de avaliacoes na hash de cada prefixo
	for tup in Trie.movie_list:
		filme = hashh.sch_hash(hash_table, tup[1])
		if filme.num_aval == 0:
			t.add_row([str(filme.movieid), tup[0], str(filme.generos), str("{:.2f}".format(filme.raiting)), str(filme.num_aval)])
		else:
			t.add_row([str(filme.movieid), tup[0], str(filme.generos), str("{:.2f}".format(filme.raiting/filme.num_aval)), str(filme.num_aval)])
	print(t)
	
	# limpa lista de prefixos
	Trie.movie_list.clear()


""" Tratamento do comando 'user' """
def user(special_list, hash_table, usuario):
	x = PrettyTable()
	x.field_names = ["user_rating", "title", "global_rating", "count"]
	
	filmes = special_list[usuario][0] 	# filmes recebe lista de filmes avaliados pelo usuario
	rat = special_list[usuario][1]		# rat recebe lista de avaliacoes feita de cada filme
	
	# pega os dados rating e num aval de cada filme na hash
	for i in range(len(filmes)):
		rating_filme = hashh.sch_hash(hash_table, filmes[i])
		
		if rating_filme.num_aval != 0:
			x.add_row([str(rat[i]), rating_filme.filme, str("{:.2f}".format(rating_filme.raiting/rating_filme.num_aval)), str(rating_filme.num_aval)])
		else:
			x.add_row([str(rat[i]), rating_filme.filme, str("{:.2f}".format(rating_filme.raiting)), str(rating_filme.num_aval)])
			
	print(x)

""" Tratamento do comando 'top' """
def top(ordered, numtop, genero_pesquisa):
	
	aval_1000 = []											# lista auxiliar pra armazenar top de genero
	t = PrettyTable(['title','genres','rating','count'])
	
	# pega todos os filmes do genero com avaliacoes acima de 1000
	for dado in ordered:
		if dado.num_aval >= 5:
			lista_generos = dado.generos.upper().split('|')
			if genero_pesquisa in lista_generos:
				aval_1000.append(dado)
				
	# divide o rating por num de aval para ter a media
	for data in aval_1000:
		if data.num_aval != 0:
			data.raiting = data.raiting/data.num_aval
	
	#ordena pelo rating
	aval_1000.sort(key=lambda data: data.raiting, reverse=True)
	
	# comeca a retirar o top genero
	limite = numtop
	for i in range(numtop):
		if aval_1000:
			t.add_row([aval_1000[i].filme, aval_1000[i].generos, str("{:.2f}".format(aval_1000[i].raiting)), aval_1000[i].num_aval])
		
	# multipica novamente o rating pois modificou o rating das estruturas na referencia
	for data in aval_1000:
		if data.num_aval != 0:
			data.raiting = data.raiting*data.num_aval
	print(t)
	return

""" Tratamento comando 'tags' """
def tags(hashtag,lista_tags, hashtable):
	lista = []
	finallist=[]
	
	t = PrettyTable(['title','genres','rating','count'])
	
	# armazena a lista de filmes com cada tag fornecida pelo usuario
	for tag in lista_tags:
		nlist = find_tag(hashtag, (re.sub('[^A-Za-z0-9]+', '', tag)).upper())
		lista.append(nlist)

	# testa o tamanho da lista 
	if lista:
		if len(lista) > 1:
			# verifica se cada filme de uma lista de tags esta em todas as outras
			for filme in lista[0]:
				havetags = True
				for listafilme in lista[1:]:
					if filme not in listafilme: # se o filme nao esta na outra lista de tags ja era
						havetags = False
						break
					else:
						continue #senao continua pesquisando
				if havetags:
					finallist.append(filme)
			
		else:	# lista tem tamanho 1
				# apenas mostra a lista ao usuario
			for filmeid in lista[0]:
				dadosfilme = hashh.sch_hash(hashtable, filmeid)
				if dadosfilme.num_aval == 0:
					t.add_row([dadosfilme.filme, dadosfilme.generos, str("{:.2f}".format(dadosfilme.raiting)), dadosfilme.num_aval])
				else:
					t.add_row([dadosfilme.filme, dadosfilme.generos, str("{:.2f}".format(dadosfilme.raiting/dadosfilme.num_aval)), dadosfilme.num_aval])
				
	
	if finallist:
		# se existir algum filme com as tags 
		for filmeid in finallist:
			dadosfilme = hashh.sch_hash(hashtable, filmeid)
			if dadosfilme.num_aval == 0:
				t.add_row([dadosfilme.filme, dadosfilme.generos, str("{:.2f}".format(dadosfilme.raiting)), dadosfilme.num_aval])
			else:
				t.add_row([dadosfilme.filme, dadosfilme.generos, str("{:.2f}".format(dadosfilme.raiting/dadosfilme.num_aval)), dadosfilme.num_aval])
	print(t)
		

# funcao de console
def menu(hash_table, special_list, ordered, hashtag):
	flag = 0
	lista_tags = []
	while True:
		comando = input("Digite a pesquisa que deseja fazer : ")
		pega_texto = comando.split(" ")
		pega_tags = comando.split("'")
		
		# se comando e vazio, indica invaldo
		if comando == "":
			print("Ops ! Comando inválido1 ! \n")
		
		elif comando[0:5] == "movie":
			if comando[5:] == "":
				print("Ops ! Comando inválido2 ! \n")

			elif (comando[5:].isspace() == True):
				print("Ops ! Comando inválido3 ! \n")

			elif len(pega_texto[0])>5:
				print("Ops ! Comando inválido4 ! \n")
			else:
				filme = comando[6:]
				# procura todos os filmes com aquele prefixo
				movie(Trie.movie_list, hash_table, filme)
				
		elif comando[0:4] == "user":
			if comando[4:] == "":
				print("Ops ! Comando inválido6 ! \n")

			elif comando[4:].isspace() == True:
				print("Ops ! Comando inválido7 \n")

			elif comando[5:].isdigit() == True:
				# chama funcao de tratamento de user
				usuario = comando[5:]
				user(special_list, hash_table, int(usuario))
			else:
				print("Ops ! Comando inválido8 ! \n")
				
		elif comando[0:3] == "top":
			if pega_texto[0][3:].isdigit() != True:
				print("Ops ! Comando inválidoooo ! \n")
			elif comando[4:] == "":
				print("Ops ! Comando inválido 11 ! \n")

			elif comando[4:].isspace() == True:
				print("Ops ! Comando inválido 12 ! \n")

			elif len(pega_texto) >= 3:
				print("Ops ! Comando inválido ! ! \n")
			else:
				# chama funcao de tratamento de top 
				numero_top = pega_texto[0][3:]
				genre = pega_texto[1].upper()
				top(ordered, int(numero_top), genre)
	
		elif comando[0:4] == "tags":
			if comando[4:] == "":
				print("Ops ! Comando inválido!")
			elif comando[4:].isspace() == True:
				print("Ops ! Comando inválido!")
			else:
				for j in pega_tags:
					if j != "" and j.isspace() != True:
						lista_tags.append(j)
				del (lista_tags[0])
				
				tags(hashtag, lista_tags, hash_table)
				lista_tags.clear()
			
		elif comando[0:4] == "exit":
			if comando[4:] == "":
				if len(pega_texto[0]) <= 4:
					print("Saindo...")
					break
				else:
					print("Comando invalido 16.\n")
			else:
				print("Comando invalido.\n")
		else:
			print("Comando invalido.\n")
