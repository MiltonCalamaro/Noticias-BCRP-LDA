## funcion para obtener la representacion vectorial de cada documento usando word2vec
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
def vectorization_word2vec(texts, modelo):
  vect_prom_total=[]
  for text in texts:
      vect_prom = searh_vect_prom(text,modelo)
      vect_prom_total.append(vect_prom)
  vect_prom_total=np.asarray(vect_prom_total)
  return vect_prom_total
def searh_vect_prom(doc,modelo):
    w2v = []
    for word in doc:
        if word in modelo.wv.vocab:
            w2v.append(modelo.wv[word])          
    vect_prom = np.mean(w2v, axis = 0)
    return vect_prom

def get_word2vec(modelo):
  palabra2vector=[]
  for i in modelo.wv.vocab:
      palabra2vector.append(modelo.wv[i])
  palabra2vector=np.array(palabra2vector) 
  return palabra2vector

def kmeans_word2vec(modelo,k=10):
  palabra2vector=get_word2vec(modelo)
  scaler = StandardScaler() 
  scaler.fit(palabra2vector)###obtiene el valor de la media y la desviacion estandar
  palabra2vector = scaler.transform(palabra2vector)
  kmeans = KMeans(n_clusters=k, random_state=0).fit(palabra2vector)
  return [kmeans,scaler,palabra2vector]

##buscamos el vector promedio para cada modelo 
def vectorization_boew(texts,modelo,scaler,kmeans,k):
    vect_boew=[]
    for text in texts:
      vector_palabra=[]
      dictionary={}
      for i in range(k):
        dictionary[i]=0
      for i in text:
          if i in modelo.wv.vocab:
              vector_palabra.append(modelo.wv[i])   
      pred_clust = kmeans.predict(scaler.transform(np.array(vector_palabra)))
      for i in pred_clust:
          dictionary[i]=dictionary[i]+1
      vect_boew.append(list(dictionary.values()))
    return vect_boew