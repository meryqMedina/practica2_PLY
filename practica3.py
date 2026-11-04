# practica3.py
import nltk
import spacy
from nltk.tokenize import WordPunctTokenizer, TweetTokenizer
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("spanish")
nlp = spacy.load("es_core_news_sm")

TEXTO = (
    "Las estudiantes María y Ángela compraron un abrigo en https://www.stradivarius.com el 04 de noviembre de 2026. "
    "Tras la compra, acudió cerca de la tienda principal con el descuento #ModaStradi. "
    "El dependiente cobró cada prenda con rapidez."
)

doc = nlp(TEXTO)

print("PARTE A")
print(WordPunctTokenizer().tokenize(TEXTO))
print(TweetTokenizer().tokenize(TEXTO))

print("\nPARTE B")
for p in TweetTokenizer().tokenize(TEXTO):
    if p.isalpha():
        s = stemmer.stem(p)
        if s != p.lower():
            print(p, "->", s)

print("\nPARTE C")
for t in doc:
    print(t.text, "|", t.lemma_, "|", t.pos_)

print("\nPARTE D")
for t in doc:
    if t.text.lower() in ["compró", "abrigo", "noviembre", "acudió", "dependiente"]:
        print(t.text, "|", stemmer.stem(t.text), "|", t.lemma_)

print("\nPARTE E")
etiquetas = [(t.text, t.pos_) for t in doc]
regla = nltk.RegexpParser("FECHA: {<NUM><ADP><NOUN><ADP><NUM>}")
print(regla.parse(etiquetas))

print("\nPARTE F")
for ent in doc.ents:
    print(ent.text, "->", ent.label_)

print("\nPARTE G")
print("Frase 1:")
for t in nlp("Acudió cerca de la tienda principal."):
    if t.text.lower() == "cerca":
        print(t.text, t.pos_)

print("Frase 2:")
for t in nlp("La cerca de madera delimitaba el jardín."):
    if t.text.lower() == "cerca":
        print(t.text, t.pos_)