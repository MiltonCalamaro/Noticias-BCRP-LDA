import re
def clean_text_noticias(news):
    clean_news = []
    for new in news:
        sin_guiones=re.sub('(\S)-\n', r'\1', new.lower()) ### sin guiones
        sin_character = re.sub(r'[^\w\s]', '', sin_guiones) ##busca los signos, caracteristicas especiales
        sin_numero = re.sub("\d+", "", sin_character)##busca los numeros y los elimina
        sin_tildes=sin_numero.translate(str.maketrans('áéíóúü','aeiouu'))
        sin_tildes = " ".join([i.strip() for i in sin_tildes.split() if len(i)>2])##solo palabras que tengan mas de tres caracteres
        clean_news.append(sin_tildes)     
    return clean_news

def remove_stopwords(news, stopwords):
    sin_stopwords=[]
    for new in news:
        content=[word for word in new.split() if word not in stopwords]
        sin_stopwords.append(" ".join(content))
    return sin_stopwords




