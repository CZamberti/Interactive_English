#!/usr/bin/python
# -*- coding: utf-8 -*-
#importazione delle librerie e delle classi necessarie
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import re
import nltk
from nltk.corpus import PlaintextCorpusReader
import collections
from collections import OrderedDict
import random
#creazione di un'istanza dell'applicazione
app = Flask(__name__)
#inizializzazione di Bootstrap
Bootstrap(app)
#creazione dell'oggetto per il menù di navigazione
nav = Nav()
#definizione della route e della funzione view per il menù di navigazione
@nav.navigation()
def mynavbar():
  return Navbar(
	View('Home', 'index'),
	View('Analisi grammaticale', 'analisi_grammaticale'),
	View('Genera, ascolta e ripeti!', 'genera_parola'),
	View('Informazioni', 'about')
  )
nav.init_app(app)

#definizione della route e della funzione view per la homepage
@app.route('/') 
def index():
	return render_template('index.html',title="Home")

#definizione della route e della funzione view per il gioco dell'analisi grammaticale
@app.route('/analisi_grammaticale', methods=['GET', 'POST']) #definizione dei metodi
def analisi_grammaticale():
	#definizione di variabili e liste vuote
	raw, lungfrase="", 0
	postag, dictionary={}, {}
	parole, partedisc=[], []
	if request.method == 'POST':
		raw = request.form.get('analisi_grammaticale')
		nltk.data.path.append('./nltk_data/')  
		#definizione del percorso della cartella nltk_data
		testo_tokenizzato = nltk.word_tokenize(raw)
		nonPunct = re.compile('.*[A-Za-z0-9].*')
		#definizione dell'espressione regolare per escludere la punteggiatura
		tes_tok_nopunt = [w for w in testo_tokenizzato if nonPunct.match(w)]#parole senza punteggiatura
		lungfrase = len(tes_tok_nopunt)
		#creazione della variabile con il testo annotato
		postag=nltk.pos_tag(tes_tok_nopunt)
		#creazione delle due liste nelle quali inserire la parola e il pos corrispondente
		for n in postag:
			parole.append(n[0])
			partedisc.append(n[1])

		#cambio le etichette delle parti del discorso in stringhe più "leggibili"
		for n,i in enumerate(partedisc):
			if i=="CC":
				partedisc[n]="Congiunzione"
			if i=="CD":
				partedisc[n]="Numero"
			if i=="DT":
				partedisc[n]="Articolo"
			if i=="EX":
				partedisc[n]="'There' esistenziale"
			if i=="FW":
				partedisc[n]="Parola straniera"
			if i=="IN":
				partedisc[n]="Preposizione"
			if i=="JJ":
				partedisc[n]="Aggettivo"
			if i=="JJR":
				partedisc[n]="Aggettivo"
			if i=="JJS":
				partedisc[n]="Aggettivo"
			if i=="LS":
				partedisc[n]="Simbolo"
			if i=="MD":
				partedisc[n]="Modale"
			if i=="NN":
				partedisc[n]="Nome"
			if i=="NNS":
				partedisc[n]="Nome"
			if i=="NNP":
				partedisc[n]="Nome"
			if i=="NNPS":
				partedisc[n]="Nome"
			#aggettivo indefinito, ma talvolta pr. possessivo
			if i=="PDT":
				partedisc[n]="Aggettivo"
			if i=="POS":
				partedisc[n]="Possessivo"
			if i=="PRP":
				partedisc[n]="Pronome"
			if i=="PRP$":
				partedisc[n]="Pronome"
			if i=="RB":
				partedisc[n]="Avverbio"
			if i=="RBR":
				partedisc[n]="Avverbio"
			if i=="RBS":
				partedisc[n]="Avverbio"
			if i=="RP":
				partedisc[n]="Particella"
			if i=="SYM":
				partedisc[n]="Simbolo"
			if i=="TO":
				partedisc[n]="'To' per infinito"
			if i=="UH":
				partedisc[n]="Esclamazione"
			if i=="VB":
				partedisc[n]="Verbo"
			if i=="VBD":
				partedisc[n]="Verbo"
			if i=="VBG":
				partedisc[n]="Verbo"
			if i=="VBN":
				partedisc[n]="Verbo"
			if i=="VBP":
				partedisc[n]="Verbo"
			if i=="VBZ":
				partedisc[n]="Verbo"
			if i=="WDT":
				partedisc[n]="Avverbio"
			if i=="WP":
				partedisc[n]="Pronome"
			if i=="WP$":
				partedisc[n]="Pronome"
			if i=="WRB":
				partedisc[n]="Avverbio"

	#compressione delle due liste con i relativi indici in un dizionario ordinato
	#Sfruttando enumerate, si ottengono tutte le occorrenze anche se doppie
	dictionary = OrderedDict(zip(enumerate(parole), partedisc))
	return render_template('analisi_grammaticale.html',title="Analizza la frase!",raw=raw, lungfrase=lungfrase, dictionary=dictionary)

#definizione della route e della funzione view per l'attività di sorting della parola casuale
@app.route('/genera_parola') 
def genera_parola():
	# apertura del vocabolario sulla casa 
	home=open('vocabolari/voc_home.txt','rU')
	# apertura del vocabolario sul cibo
	food=open('vocabolari/voc_food.txt','rU')
	# apertura del vocabolario sui numeri e colori
	numcol=open('vocabolari/voc_num_col.txt','rU')
	# apertura del vocabolario sui vestiti
	clothes=open('vocabolari/voc_clothing.txt','rU')
	# apertura del vocabolario sulle parti del corpo
	part_body=open('vocabolari/voc_pobody.txt','rU')
	# apertura del vocabolario sulla scuola
	school=open('vocabolari/voc_school.txt','rU')
	# apertura del vocabolario sulla città
	city=open('vocabolari/voc_city.txt','rU')

	#lettura i dati in input
	rawh=home.read()
	rawf=food.read()
	rawnc=numcol.read()
	rawcl=clothes.read()
	rawpb=part_body.read()
	rawsc=school.read()
	rawcy=city.read()

	#divisione del testo in token
	tes_tok_sh = nltk.word_tokenize(rawh)
	tes_tok_sf = nltk.word_tokenize(rawf)
	tes_tok_snc = nltk.word_tokenize(rawnc)
	tes_tok_scl = nltk.word_tokenize(rawcl)
	tes_tok_spb = nltk.word_tokenize(rawpb)
	tes_tok_sco = nltk.word_tokenize(rawsc)
	tes_tok_cy = nltk.word_tokenize(rawcy)

	#sostituzione dello spazio all'underscore nelle parole composte e creazione delle liste con le parole per ogni categoria
	parole_home = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_sh]
	parole_food = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_sf]
	parole_numcol = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_snc]
	parole_cl = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_scl]
	parole_pb = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_spb]
	parole_sc = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_sco]
	parole_cy = [re.sub(r'(\w*)_(\w*)',r'\1 \2', w) for w in tes_tok_cy]

	return render_template('genera_parola.html',title="Genera, ascolta e ripeti!", parole_home=parole_home, parole_food=parole_food, parole_numcol=parole_numcol, parole_cl=parole_cl, parole_pb=parole_pb, parole_sc=parole_sc, parole_cy=parole_cy)
#definizione della route e della view della pagina delle informazioni
@app.route('/about')
def about():
	return render_template('about.html', title="Informazioni")
	
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")