from project import app, db, debug

if __name__ == '__main__':
  app.run(debug=debug, port=3001)
