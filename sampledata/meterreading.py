import couchdb
couch = couchdb.Server("http://41.79.111.110:5984/")
db = couch['h2mobile']

map_fun = '''function(doc) {
     if (doc.type == 'meterreading')
         emit(doc, null);
}'''
for doc in db.query(map_fun):
    db.delete(doc.key)



db.create({
   "type": "meterreading",
   "meterno": "0101010101",
   "meterreading": 100,
   "username": "Klaas",
   "readingdate":"2011-12-03 16:00:00"
})
db.create({
   "type": "meterreading",
   "meterno": "0101010102",
   "meterreading": 200,
   "username": "Klaas",
   "readingdate":"2011-12-03 16:00:00"
})
db.create({
   "type": "meterreading",
   "meterno": "0101010103",
   "meterreading": 300,
   "username": "Klaas",
   "readingdate":"2011-12-03 16:00:00"
})
db.create({
   "type": "meterreading",
   "meterno": "0101010104",
   "meterreading": 100,
   "username": "Schalk",
   "readingdate":"2011-12-03 16:00:00"
})

