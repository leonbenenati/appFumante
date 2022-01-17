import streamlit as st 
import pandas as pd
import pickle
import base64


paginas = ['Pagina inicial', 'Análise rapida','Análise com arquivo']
pagina = st.sidebar.radio('Selecione uma página', paginas)

if pagina == 'Pagina inicial':
	st.title("Será que a pessoa fuma?")
	st.subheader('By Leon Emiliano Benenati')
	st.subheader('Para saber se a pessoa é fumante Selecione uma pagina ao lado, a primeira é uma análise rapida a segunda é com um arquivo CSV')
	st.markdown('---')


if pagina == 'Análise rapida':
	st.subheader(' A pessoa é fumante?')
	st.subheader('Insira os dados da pessoa e descubra')
	st.markdown('---')

	idade = st.slider('Entre com a idade:', 18, 80, 30)
	sexo = st.selectbox("Sexo da pessoa", ['Mulher', 'Homem'])
	if sexo == "Homem":
		sexo = 1
	else:
		sexo = 0
	imc = st.number_input('Entre com o IMC')
	filhos = st.selectbox("Selecione a quantidade de filhos(se for mais de 4 filhos selecione 3)", [0, 1, 2, 3])
	custos = st.number_input('Entre custos de seguro:')/10000
	regiao = st.selectbox("Região da pessoa", ['northwest', 'northeast','southeast','southwest'])
	
	regiao_northwest=[]
	if regiao == "northwest":
		regiao_northwest = 1
	else:
		regiao_northwest = 0

	regiao_southeast=[]
	if regiao == "southeast":
		regiao_southeast = 1
	else:
		regiao_southeast = 0

	regiao_southwest=[]
	if regiao == "southwest":
		regiao_southwest = 1
	else:
		regiao_southwest = 0

	dados_dicio = {'Idade': [idade], 'IMC': [imc], 'Filhos': [filhos],'Custos': [custos],'Sexo_male': [sexo], 
			'Regiao_northwest': [regiao_northwest],'Regiao_southeast': [regiao_southeast],
			'Regiao_southwest': [regiao_southwest]}

	
	dados = pd.DataFrame(dados_dicio)
	#st.write(dados)

	if st.button('CLIQUE AQUI PARA DESCOBRIR SE A PESSOA FUMA'):
		with open('modelo_escolhido', 'rb') as f:  
			model = pickle.load(f)
			saida = model.predict(dados)
		
	if saida == 0:
		("Não fumante")
	else:
		("Fumante")


if pagina == 'Análise com arquivo':
	st.title("Carregue seu arquivo")

	uploaded_file = st.file_uploader("Choose a file")
	if uploaded_file is not None:
		df1 = pd.read_csv(uploaded_file)
		df2=df1
	st.write(df1)

	if st.button('CLIQUE AQUI PARA DESCOBRIR SE A PESSOA FUMA'):
		def auxiliar(x):
			if x == 0:
				return 0
			elif x ==1:
				return 1
			elif x ==2:
				return 2
			else:
				return 3
			df1['Filhos'] = df1['Filhos'].apply(auxiliar)
		variaveis = ["Sexo", "Fumante","Regiao"]
		df1 = pd.get_dummies(df1, columns = variaveis, drop_first = True)
		df1['Custos'] = df1['Custos']/10000
		X = df1[['Idade','IMC',"Filhos","Custos","Sexo_male","Regiao_northwest","Regiao_southeast","Regiao_southwest"]]
		with open('modelo_escolhido', 'rb') as f:  
			model = pickle.load(f)
			pred = model.predict(X)
		previsao = pd.DataFrame()
		previsao['fumante?'] = pred
		df_final = pd.concat([df2,previsao],axis=1)
		def fun(x):
			if x == 1:
				return 'Sim'
			else:
				return 'Não'
		df_final['fumante?'] = df_final['fumante?'].apply(fun)
	st.write(df_final)

	csv = df_final.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()
	href = f'<a href="data:file/csv;base64,{b64}" download="Arquivo.csv">Clique para salvar o arquivo</a>'
	st.markdown(href, unsafe_allow_html=True)

