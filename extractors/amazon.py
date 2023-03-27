from selectorlib import Extractor


def get_amazon_extractor():
  return Extractor.from_yaml_string("""
    product:
      css: div.a-fixed-left-grid-col.product-info
      type: Text
      children:
        title:
          css: 'h1.a-size-large a.a-link-normal'
          type: Text
        link:
          css: 'h1.a-size-large a.a-link-normal'
          type: Link

    reviews:
      css: 'div.a-row div.a-section.celwidget'
      multiple: True
      type: Text
      children:
        title:
          css: a.a-size-base span
          type: Text
        content:
          css: div.a-row.a-spacing-small.review-data
          type: Text
        reviewee:
          css: 'span.a-profile-name'
          type: Text
        verified:
          css: 'span[data-hook="avp-badge"]'
          type: Text
        rating:
          css: 'div.a-row:nth-of-type(2) a.a-link-normal:nth-of-type(1)'
          type: Text
    next_link:
      css: 'li.a-last a'
      type: Link
    """)

def sanitize_rating(rating):
  return float(rating.replace('out of 5 stars', ''))

def sanitize_reviewee(reviewee):
  return reviewee.replace('Reviewed in the .* on', '')

def sanitize_verified_purchase(verified):
  return verified is not None

def sanitize_next_link(next_link):
  return f'https://www.amazon.in{next_link}'

def sanitize_amazon_data(raw_data):
  extractor = get_amazon_extractor();
  data = extractor.extract(raw_data)
  if data['reviews'] is None:
    return None

  for review in data['reviews']:
    if 'rating' in review:
      review['rating'] = sanitize_rating(review['rating'])
    
    if 'reviewee' in review:
      review['reviewee'] = sanitize_reviewee(review['reviewee'])
    
    if 'verified' in review:
      review['verified'] = sanitize_verified_purchase(review['verified'])
    
  if 'next_link' in data:
    if ('signin' not in data['next_link']):
      data['next_link'] = sanitize_next_link(data['next_link'])
  return data
