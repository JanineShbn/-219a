import jsonlines
import nltk
import matplotlib.pyplot as plt
from collections import Counter

# Legislatur 19
legislatur = 19

# Leere Liste generieren
alleReden = []

with jsonlines.open(f"C:/Users/User/Desktop/Politische Debatten/data/speeches_19.jsonl") as f:
    for line in f.iter():
        alleReden.append(line)

# Nach Datum sortieren
alleReden.sort(key=lambda x: x["date"])

## Zunächst brauchen wir eine Funktion, die uns die Reden gibt, die ein bestimmtes Wort enthalten.
#  Funktion für Textsuche:
#  Gibt eine Untermenge an Reden zurück, die einen bestimmten String (Wort) enthalten.

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

wort = "Abtreibung"

#  Hier rufen wir die Suchfunktion auf und speichern die Untermenge der Reden.
untermenge = find_speeches_with_word(wort, alleReden)
satz_liste = find_sentences_with_word(wort,untermenge)

print(f'In {len(untermenge)} Reden gibt es {len(satz_liste)} Sätze, die {wort} enthalten:')

# Schleife, um die relevanten Informationen aus den Reden zu extrahieren und zur input_list hinzuzufügen
input_list = [speech['name'] for speech in untermenge]

# Verwenden Sie Counter, um die Häufigkeit der Namen zu zählen
häufigkeiten = Counter(input_list)

# Anzeigen der Namen und ihrer Häufigkeiten
for name, häufigkeit in häufigkeiten.items():
    print(f'{name}: {häufigkeit} Reden')

# Sortieren Sie die Ergebnisse nach der Häufigkeit absteigend und wählen Sie die Top-N-Politikerinnen aus
top_n = 10  # Anzahl der Top-Politikerinnen, die im Histogramm angezeigt werden sollen
top_politikerinnen = dict(häufigkeiten.most_common(top_n))

# Extrahieren Sie die Namen und die entsprechenden Häufigkeiten der Top-Politikerinnen
namen = list(top_politikerinnen.keys())
häufigkeiten_werte = list(top_politikerinnen.values())

# Erstellen Sie eine benutzerdefinierte Farbpalette für die Balken
farben = ['black', 'limegreen', 'blue', 'black', 'blue', 'red', 'mediumvioletred', 'blue', 'yellow', 'blue']

# Erstellen Sie das Histogramm für die Top-Politikerinnen und weisen Sie jedem Balken eine Farbe aus der Farbpalette zu
plt.figure(figsize=(12, 6))
plt.barh(namen, häufigkeiten_werte, color=farben)
plt.xlabel('Anzahl der Reden')
plt.ylabel('Politikerinnen')
plt.title(f'Top-{top_n} Politikerinnen mit höchstem Redeanteil zu "{wort}" in der 19. Legislaturperiode')
plt.gca().invert_yaxis()  # Um die Politikerinnen mit der höchsten Häufigkeit oben anzuzeigen

# Anzeigen des Histogramms
plt.show()
