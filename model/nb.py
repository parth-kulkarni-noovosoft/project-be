import json
from math import exp, sqrt, pi
from pprint import pprint

BOW = {}

def load_data():
    with open('labelled_data.json') as json_input:
        data = json.load(json_input)
    
    split_index = int(len(data) * 0.8)
    train_data = data[:split_index]
    test_data = data[split_index:]
    
    return train_data, test_data

def get_full_review_text(review):
    return review['title'] + " " + review['content']


def vectorize_text(text):
    words = text.lower().split()
    vector = [0] * len(BOW)
    for word in words:
        if word in BOW:
            vector[BOW[word]] = 1
    
    return vector

def build_vocab(data):
    global BOW
    for review in data:
        words = get_full_review_text(review).lower().split(' ')
        for word in words:
            if word not in BOW:
                BOW[word] = len(BOW)

def separate_by_class(dataset):
    data_by_class = {}
    for row in dataset:
        class_value = row[-1]
        if class_value not in data_by_class:
            data_by_class[class_value] = []
        data_by_class[class_value].append(row)
    return data_by_class

mean = lambda nums: sum(nums) / len(nums)
stdev = lambda nums: (sum([(x - mean(nums)) ** 2 for x in nums]) / (len(nums) - 1)) ** 0.5

def calculate_gaussian_probability(x, mean, stdev):
    if stdev == 0:
        return 1 if x == mean else 0
    exponent = exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
    return (1 / (sqrt(2 * pi) * stdev)) * exponent

def summarize_dataset(dataset):
    num_columns = len(dataset[0])
    summaries = []

    for i in range(num_columns-1):
        column_values = [row[i] for row in dataset]
        summaries.append([mean(column_values), stdev(column_values), len(column_values)])
    return summaries

def get_class_column_summary(dataset):
    data_by_class = separate_by_class(dataset)
    summaries = {}
    for class_value, rows in data_by_class.items():
        summaries[class_value] = summarize_dataset(rows)
    return summaries

def calculate_class_probabilities(summaries, row):
    get_len_from_summaries = lambda label: summaries[label][0][2]

    total_rows = float(sum([get_len_from_summaries(label) for label in summaries]))
    probabilities = {}
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = get_len_from_summaries(class_value)/total_rows
        for i, summary in enumerate(class_summaries):
            mean, stdev, _ = summary
            probabilities[class_value] *= calculate_gaussian_probability(row[i], mean, stdev)
    return probabilities

def get_guess(class_probabilities):
    return max(class_probabilities, key=lambda k: class_probabilities[k])

def test_with_data(summaries, dataset):
    answers = [row[-1] for row in dataset]
    guesses = []

    for row in dataset:
        probabilities = calculate_class_probabilities(summaries, row)
        guesses.append(get_guess(probabilities))

    result = calculate_confusion_matrix(answers, guesses)
    calculate_and_print_performance_metrics(result)
    return result

def sanitize_data(data):
    dataset = []
    for review in data:
        vector = vectorize_text(get_full_review_text(review))
        dataset.append([*vector, review['rating'], review['authentic']])
    return dataset


def train_model(data):
    dataset = sanitize_data(data)
    summaries = get_class_column_summary(dataset)
    return summaries

def calculate_confusion_matrix(answers, guesses):
    confusion_matrix = {
        'TP': 0,
        'TN': 0,
        'FP': 0,
        'FN': 0
    }

    for answer, guess in zip(answers, guesses):
        if answer == True and guess == True:
            confusion_matrix['TP'] += 1
        elif answer == True and guess == False:
            confusion_matrix['FN'] += 1
        elif answer == False and guess == True:
            confusion_matrix['FP'] += 1
        elif answer == False and guess == False:
            confusion_matrix['TN'] += 1

    return confusion_matrix

def calculate_and_print_performance_metrics(result):
    accuracy = (result['TP'] + result['TN']) / (result['TP'] + result['TN'] + result['FP'] + result['FN'])
    precision = result['TP'] / (result['TP'] + result['FP'])
    recall = result['TP'] / (result['TP'] + result['FN'])
    f1_score = 2 * (precision * recall) / (precision + recall)

    confusion_matrix = [
        [result['TP'], result['FN']],
        [result['FP'], result['TN']]
    ]

    print('[')
    for line in confusion_matrix:
        print(' ', line)
    print(']')

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1_score}\n")


if __name__ == '__main__':
    train_data, test_data = load_data()

    build_vocab([*train_data, *test_data])
    summaries = train_model(train_data)

    test_with_data(summaries, sanitize_data(train_data))
    test_with_data(summaries, sanitize_data(test_data))
