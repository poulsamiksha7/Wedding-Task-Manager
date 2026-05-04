from flask import Flask

app=Flask(__name__)

@app.route('/')
def home():
    return '<h1>Wedding Task MAnager</h1><p>App is Live</p>'

@app.route('/tasks')
def tasks():
    return '<h1>Task Page</h1><p>Coming Soon</p>'

if __name__=='__main__':
    app.run(debug=True)
