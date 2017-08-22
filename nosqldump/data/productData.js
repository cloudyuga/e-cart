let products = [
  db.product.insert({'_id': NumberInt(1), 'name': 'nike', 'category': 'shoe', 'price': 11, 'location': '/static/shoe.jpg'}),
  db.product.insert({'_id': NumberInt(2), 'name': 'iphone', 'category': 'mobile', 'price': 100, 'location': '/static/mobile.jpg'}),
  db.product.insert({'_id': NumberInt(3), 'name': 'titan', 'category': 'watch', 'price': 50, 'location': '/static/watch.jpeg'}),
  db.product.insert({'_id': NumberInt(4), 'name': 'philips', 'category': 'speaker', 'price': 75, 'location': '/static/speaker.jpeg'}),
  db.product.insert({'_id': NumberInt(5), 'name': 'adidas', 'category': 'tshirt', 'price': 60, 'location': '/static/tshirt.jpeg'}),
  db.product.insert({'_id': NumberInt(6), 'name': 'sony', 'category': 'tv', 'price': 1000, 'location': '/static/tv.jpg'}),
  db.product.insert({'_id': NumberInt(7), 'name': 'seagate', 'category': 'harddisk', 'price': 200, 'location': '/static/harddisk.jpg'}),
  db.product.insert({'_id': NumberInt(8), 'name': 'journal', 'category': 'book', 'price': 30, 'location': '/static/journal.jpg'})
]
