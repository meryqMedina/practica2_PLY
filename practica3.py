# practica3.py - Práctica 3: Procesamiento del Lenguaje Natural (NLTK y spaCy)
import nltk
import spacy
from nltk.tokenize import WordPunctTokenizer, TweetTokenizer
from nltk.stem.snowball import SnowballStemmer

# Inicialización de herramientas
stemmer = SnowballStemmer("spanish")
nlp = spacy.load("es_core_news_sm")

# Texto de prueba propio diseñado para cumplir los 4 requisitos:
# 1. Elemento web (URL y hashtag)
# 2. Palabra ambigua ("banco")
# 3. Entidad reconocible ("Ticketmaster")
# 4. Entidad fija (Fecha: "18 de noviembre de 2026")
TEXTO = (
    "El estudiante compró las entradas para el concierto en https://www.ticketmaster.es el 18 de noviembre de 2026. "
    "Tras la actuación, la banda tocó cerca de la entrada principal con el colectivo #MusicaEnVivo. "
    "El público banco cada canción con entusiasmo."
)

doc = nlp(TEXTO)

print("=" * 65)
print("PARTE A: TOKENIZACIÓN (WordPunctTokenizer vs TweetTokenizer)")
print("=" * 65)
tokens_wp = WordPunctTokenizer().tokenize(TEXTO)
tokens_tw = TweetTokenizer().tokenize(TEXTO)

print("\n--- WordPunctTokenizer ---")
print(tokens_wp)

print("\n--- TweetTokenizer ---")
print(tokens_tw)


print("\n" + "=" * 65)
print("PARTE B: STEMMING (SnowballStemmer)")
print("=" * 65)
print(f"{'Palabra Original':<20} -> {'Raíz (Stem)':<20}")
print("-" * 45)
for palabra in tokens_tw:
    if palabra.isalpha():
        stem = stemmer.stem(palabra)
        if stem != palabra.lower():
            print(f"{palabra:<20} -> {stem:<20}")


print("\n" + "=" * 65)
print("PARTE C: ANÁLISIS CON SPACY (Texto, Lema y POS)")
print("=" * 65)
print(f"{'Texto':<25} {'Lema':<25} {'Categoría (POS)':<15}")
print("-" * 65)
for t in doc:
    print(f"{t.text:<25} {t.lemma_:<25} {t.pos_:<15}")


print("\n" + "=" * 65)
print("PARTE D: COMPARACIÓN DE RAÍZ Y LEMA")
print("=" * 65)
palabras_interesantes = ["compró", "entradas", "noviembre", "actuación", "público"]
print(f"{'Palabra':<18} {'Raíz (NLTK)':<18} {'Lema (spaCy)':<18}")
print("-" * 55)
for t in doc:
    if t.text.lower() in palabras_interesantes:
        raiz = stemmer.stem(t.text)
        print(f"{t.text:<18} {raiz:<18} {t.lemma_:<18}")


print("\n" + "=" * 65)
print("PARTE E: EXTRACCIÓN MEDIANTE REGLAS CON RegexpParser")
print("=" * 65)
etiquetas_spacy = [(t.text, t.pos_) for t in doc]
regla_fecha = nltk.RegexpParser("FECHA: {<NUM><ADP><NOUN><ADP><NUM>}")
arbol = regla_fecha.parse(etiquetas_spacy)

print("\n1. Detección exitosa de la entidad fija en el texto original:")
for subarbol in arbol.subtrees():
    if subarbol.label() == "FECHA":
        print(subarbol)

# Ejemplo de fallo al cambiar el formato de fecha a formato numérico puro
texto_fallo = "La cita fue el 18/11/2026 en el recinto."
doc_fallo = nlp(texto_fallo)
etiquetas_fallo = [(t.text, t.pos_) for t in doc_fallo]
arbol_fallo = regla_fecha.parse(etiquetas_fallo)
coincidencias = [t for t in arbol_fallo.subtrees() if t.label() == "FECHA"]
print("\n2. Ejemplo de fallo con formato alterado ('18/11/2026'):")
print("Resultado detectado:", coincidencias)


print("\n" + "=" * 65)
print("PARTE F: ENTIDADES NOMBRADAS (doc.ents)")
print("=" * 65)
if doc.ents:
    for ent in doc.ents:
        print(f"Entidad: {ent.text:<30} | Etiqueta: {ent.label_:<10} ({spacy.explain(ent.label_)})")
else:
    print("No se detectaron entidades nombradas.")


print("\n" + "=" * 65)
print("PARTE G: CASO DE ESTUDIO - PALABRA AMBIGUA ('banco')")
print("=" * 65)
frase1 = "El público banco cada canción con entusiasmo."
frase2 = "Ingresó los ahorros en el banco central."

print(f"Frase 1: '{frase1}'")
for t in nlp(frase1):
    if t.text.lower() == "banco":
        print(f"  -> Token: '{t.text}' | POS: {t.pos_} ({spacy.explain(t.pos_)}) | Lema: {t.lemma_}")

print(f"\nFrase 2: '{frase2}'")
for t in nlp(frase2):
    if t.text.lower() == "banco":
        print(f"  -> Token: '{t.text}' | POS: {t.pos_} ({spacy.explain(t.pos_)}) | Lema: {t.lemma_}")