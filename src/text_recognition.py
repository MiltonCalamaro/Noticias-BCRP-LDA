import pytesseract
import fitz
from PIL import Image
import io
import glob
import re
from os.path import join, basename
import time
from datetime import datetime
import pandas as pd

def text_recognigtion(flist):
  start_time = time.time()
  archivo=[]
  fecha=[]
  pagina=[]
  texto=[]
  for f in flist:
      print("Procesando archivo %s" % f)
      try:
          doc = fitz.open(f)
          for i in range(len(doc)):
              aux=[]
              for img in doc.getPageImageList(i):
                  xref=img[0]
                  stream = io.BytesIO(fitz.Pixmap(doc,xref).getPNGData())
                  imagenPag = Image.open(stream)### Obtener las imágenes
                  try:
                      info=pytesseract.image_to_osd(imagenPag, lang='spa')
                      angulo = int(re.search('(?<=Rotate: )\d+', info).group(0))
                      if angulo != 0:
                          infotext="El angulo a rotar es: %s" % (angulo-180)
                          print(infotext)
                          imagenPag = imagenPag.rotate(angulo-180, expand=True)
                      aux.append(pytesseract.image_to_string(imagenPag, lang='spa'))            
                  except:
                      continue
              archivo.append(basename(f))
              fecha.append(datetime.strptime(f[-12:-4],'%Y%m%d'))
              pagina.append(i+1)
              texto.append("\n".join(aux)) 
      except:
          print("no se puede abrir el archivo {}".format(f))
          continue
  print("El tiempo transcurrido es %f segundos" % (time.time() - start_time))
  dict_={"archivo":archivo,
      "fecha":fecha,
      "pagina":pagina,
      "texto":texto}
  df=pd.DataFrame(dict_)
  return df