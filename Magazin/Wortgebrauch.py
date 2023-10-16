import jsonlines
import nltk

nltk.download('punkt')

from collections import Counter
import matplotlib.pyplot as plt


legislatur = 19

alleReden = []

with jsonlines.open(f"C:/Users/User/Desktop/Politische Debatten/data/speeches_19.jsonl") as f:
    for line in f.iter():
        alleReden.append(line)

alleReden.sort(key=lambda x: x['date'])

#Funktion für Textsuche

def find_speeches_with_word(search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if (search_term in speech['text']):
            filtered_speeches.append(speech)
    return filtered_speeches


# alle Sätze sehen, in denen der Suchbegriff vorkommt


def find_sentences_with_word(search_term, speeches):
    sents_with_word = []
    for speech in speeches:
        sent_list = nltk.sent_tokenize(speech['text'])
        for sent in sent_list:
            if search_term in sent:
                sents_with_word.append(sent)
    return sents_with_word


#  Funktion, mit der man eine Menge an Reden nach verschiedenen Kriterien filtern kann.

def filter_speeches_for(what, search_term, speeches):
    filtered_speeches = []
    for speech in speeches:
        if search_term in speech[what]:
            filtered_speeches.append(speech)

    filtered_speeches.sort(key=lambda x: x['date'])
    return filtered_speeches


# Akzeptiert Liste mit Suchwörtern
def find_speeches_with_several_words_and(words, lst):
    return [d for d in lst if all(word in d['text'] for word in words)]

# OR Condition
def find_speeches_with_several_words_or(words, lst):
    return [d for d in lst if any(word in d['text'] for word in words)]


################ Anwendung ################

such_wort1 = "Schwangerschaftsabbruch" #"Abtreibung" #"219a"

parties = ['SPD', 'FDP', 'CDU', 'LINKE', 'GRÜNEN', 'AfD']

frequencies1 = []
for party in parties:
    untermenge = find_speeches_with_word(such_wort1, alleReden)
    untermenge = filter_speeches_for('party', party, untermenge)
    print(f'Die {party} hat {len(untermenge)} Reden mit "{such_wort1}" gehalten.')
    frequencies1.append(len(untermenge))

print('\n')

#Visualisierung

plt.bar(parties, frequencies1, color=["red", "yellow", "black", "pink", "green", "blue"],label=f'{such_wort1}')
plt.title("Verteilung der Häufigkeiten")
plt.xlabel("Partei")
plt.ylabel("Anzahl der Reden")
plt.legend(loc="upper left")

plt.show()
