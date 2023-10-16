import jsonlines
import nltk

nltk.download('punkt')

from collections import Counter

legislatur = 19

#leere Liste:
alleReden = []

# Wir öffnen den entsprechende File:
with jsonlines.open(f"C:/Users/User/Desktop/Politische Debatten/data/speeches_19.jsonl") as f:
    for line in f.iter():
        # Wir packen alles Zeile für Zeile zu unserer Liste:
        alleReden.append(line)

# Wir sortieren nach Datum:
alleReden.sort(key=lambda x: x['date'])


#  Funktion für Textsuche:
def find_speeches_with_word(search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if (search_term in speech['text']):
            filtered_speeches.append(speech)
    return filtered_speeches

def find_sentences_with_word(search_term, speeches):
    sents_with_words = []
    for speech in speeches:
        sent_list = nltk.sent_tokenize(speech['text'])
        for sent in sent_list:
            if search_term in sent:
                sents_with_words.append(sent)
    return sents_with_words

wort = "219a"
untermenge = find_speeches_with_word(wort, alleReden)

##Funktion

def filter_speeches_for(what, search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if search_term in speech[what]:
            filtered_speeches.append(speech)

    filtered_speeches.sort(key=lambda x: x['date'])
    return filtered_speeches


# Suche
suche_nach = 'FDP' #'LINKE' 'GRÜNEN' 'SPD' 'CDU/CSU' 'AfD'
untermenge = filter_speeches_for('party', suche_nach, untermenge)
satz_liste = find_sentences_with_word(wort,untermenge)

print(f'In {len(untermenge)} Reden gibt es {len(satz_liste)} Sätze von {suche_nach}, die {wort} enthalten:')
print(f'\n')

# Anzeigen lassen
for sx,satz in enumerate(satz_liste):
    print(f' Satz {sx+1}: {satz}')
    print(f'\n')

from wordcloud import WordCloud
import matplotlib.pyplot as plt


text = " ".join(satz_liste)
stop_words = ["Liebe Kolleginnen", "Liebe Kollegen","Das", "Der", "Die", "da", "Sie", "Wir", "und", "Und", "eine", "einer", "von", "als", "jede", "jeder", "ein", "einem", "vom", "an", "im", "des", "zu", "sind", "welcher", "den", "Diese", "auch", "ohne", "sondern", "über", "es", "oder", "sich", "wenn", "wie", "um", "nach", "weil", "ob", "ihrer", "nur", "hat", "geht", "für", "pro", "dass", "dem", "ich", "dann", "wird", "wurde",  "unter", "vor", "dafür", "Deshalb", "ab", "etwa", "also", "mit", "so", "noch", "dazu", "auf", "ist", "schon", "würden", "aber", "einen", "doch", "in", "alle", "deren", "darum", "sein", "Damit", "man", "diesem", "zum Beispiel", "dort", "mir", "wo", "beim", "welche", "ins", "uns", "bei", "durch", "zur", "meine", "denen", "bzw", "andere", "bis", "haben"]
# Generate a word cloud image

wordcloud = WordCloud(stopwords = stop_words, background_color = "white", width=1920, height=1080, max_font_size=150).generate(text)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()