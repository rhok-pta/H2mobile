import couchdb
couch = couchdb.Server("http://41.79.111.110:5984/")
db = couch['h2mobile']

map_fun = '''function(doc) {
     if (doc.type == 'problem')
         emit(doc, null);
}'''
for doc in db.query(map_fun):
    db.delete(doc.key)



db.create({
   "type": "problem",
   "username": "Jabu",
   "tapid": "School",
   "area": "Idutijwa",
   "problem":"leaking",
   "comments":"This is a comment",
   "status":"pending",
   "reportdate":"2011-12-03 16:00:00"
})
db.create({
   "type": "problem",
   "username": "Jabu",
   "tapid": "Joe's shop",
   "area": "Idutijwa",
   "problem":"vandalised",
   "comments":"This is a comment",
   "status":"resolved",
   "reportdate":"2011-12-03 17:00:00"
})
