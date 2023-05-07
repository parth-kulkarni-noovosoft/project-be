import string
import json

WORD_POLARITY = {}


def load_sentiwordnet():
    global WORD_POLARITY

    with open("assets/SentiWordNet_3.0.0.txt", "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            
            fields = line.strip().split("\t")
            pos, neg = float(fields[2]), float(fields[3])

            words = map(lambda x: x.split('#')[0], fields[4].split(' '))
            for word in words:
                WORD_POLARITY[word] = pos - neg

def analyze_sentiment_sentiwordnet(review):
    review = review.translate(str.maketrans("", "", string.punctuation)).lower()
    words = review.split()

    return sum(WORD_POLARITY.get(word, 0) for word in words)

def load_data():
    with open('data.json') as json_input:
        return json.load(json_input)
    
def update_date_with_polarity(json_data):
    for data in json_data:
        data['polarity'] = analyze_sentiment_sentiwordnet(data['content'])
    
    return json_data

def write_to_json(updated_json_data):
    with open("labelled_sentiment_data.json", "w") as json_file:
        json.dump(updated_json_data, json_file)

def main():
    load_sentiwordnet()
    json_data = load_data()
    updated_json_data = update_date_with_polarity(json_data)
    write_to_json(updated_json_data)

if __name__ == '__main__':
    main()