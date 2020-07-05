import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.preprocessing import  StandardScaler

def plot_word2vec(modelo,word_freq,size_figure=(15,10)):
  palabra2vector=[]
  for i in modelo.wv.vocab:
      palabra2vector.append(modelo.wv[i])  
  ##analisis de componentes
  palabra2vector=np.array(palabra2vector)
  scaler=StandardScaler()
  palabra2vector=scaler.fit_transform(palabra2vector)

  pca = PCA(n_components=2).fit(palabra2vector)
  pca_2d = pca.transform(palabra2vector)

  ## crear el df de la palabras con sus respectivos vectores
  w2v_df=pd.DataFrame(pca_2d, columns=["x1","x2"])
  w2v_df["word"]=modelo.wv.vocab
  w2v_df=w2v_df.set_index("word")
  w2v_df=w2v_df.loc[word_freq,:]
  w2v_df.head()

  ## visualizacion de las relaciones entre palabras
  plt.figure(figsize=size_figure)
  for word, x1, x2 in zip(w2v_df.index, w2v_df['x1'], w2v_df['x2']):
      plt.annotate(word, (x1,x2 ))  
  PADDING = 1.0
  x_axis_min = np.amin(pca_2d, axis=0)[0] - PADDING
  y_axis_min = np.amin(pca_2d, axis=0)[1] - PADDING
  x_axis_max = np.amax(pca_2d, axis=0)[0] + PADDING
  y_axis_max = np.amax(pca_2d, axis=0)[1] + PADDING
  plt.xlim(x_axis_min,x_axis_max)
  plt.ylim(y_axis_min,y_axis_max)
  plt.show()