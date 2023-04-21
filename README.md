# Fake Product Review Detection and Sentiment Analysis

This project aims to create software that allows the detection of fake reviews and also allow the users to find the overall sentiment of the reviews of any product.

## Usage

Requirements:
- Python v3.8
- Pip v20.0.2

### Installation

```
pip install -r requiements.txt
```

### Scraping
- Put the URL of any product in the `urls.txt`
- Run the following command

```
python main.py
```

The scraped reviews will be put inside the `data.json`

### Classification
- Given you have labelled data in `data.json`
- Run the following command

```
python model/nb.py
```