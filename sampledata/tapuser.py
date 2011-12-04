import couchdb
couch = couchdb.Server("http://41.79.111.110:5984/")
db = couch['h2mobile']
db.create({
   "type": "usertap",
   "tapid": "Gogo's place",
   "area": "Idutijwa",
   "username": "Jabu"
})
db.create({
   "type": "usertap",
   "tapid": "School",
   "area": "Idutijwa",
   "username": "Jabu"
})
db.create({
   "type": "usertap",
   "tapid": "Joe's shop",
   "area": "Idutijwa",
   "username": "Jabu"
})
db.create({
   "type": "usertap",
   "tapid": "Main road",
   "area": "Idutijwa",
   "username": "Klaas"
})

