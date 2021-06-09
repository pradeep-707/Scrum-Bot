from mongoengine import connect

def connectDb(mongoUri):
  connect(host=mongoUri)
