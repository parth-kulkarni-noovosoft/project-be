from .amazon import sanitize_amazon_data

class Extractor:
  def amazon(self, data):
    return sanitize_amazon_data(data)