import couchdb
couch = couchdb.Server("http://41.79.111.110:5984/")

db = couch['h2mobile']

map_fun = '''function(doc) {
     if (doc.type == 'meteruser')
         emit(doc, null);
}'''
for doc in db.query(map_fun):
    db.delete(doc.key)


db = couch['h2mobile']
db.create({
   "type": "meteruser",
   "meterno": "0101010101",
   "username": "Klaas"
})
db.create({
   "type": "meteruser",
   "meterno": "0101010102",
   "username": "Klaas"
})
db.create({
   "type": "meteruser",
   "meterno": "0101010103",
   "username": "Klaas"
})
db.create({
   "type": "meteruser",
   "meterno": "0101010104",
   "username": "Schalk"
})
