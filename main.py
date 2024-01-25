from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import json
from flask_sitemap import Sitemap

app = Flask(__name__)
sitemap = Sitemap(app=app)
limiter = Limiter(app, default_limits=["5 per second"])


def open_otzivi():
  with open('revies.json', 'r') as f:
    return json.load(f)

def get_servers():
  try:
    server = requests.get('https://64d47985-9dac-47db-9899-4f1b76fafa2f-00-gd6hsoma9f0t.picard.replit.dev/').json()
    uses_guilds = server['uses_guilds']
    uses = server['uses']
    commands = server['commands']
  
    return {'uses': uses, 'uses_guilds': uses_guilds, 'commands': commands}
  except:
    return 'Информация не доступна'

@app.route('/')
def online():
    info = get_servers()
    uses_guilds = 'не доступно'
    uses = 'не доступно'
    commands = 'не доступно'
    if info != 'Информация не доступна':
      uses_guilds = info['uses_guilds']
      uses = info['uses']
      commands = info['commands']
    reviews = reversed(open_otzivi())
    print(reviews)
    return render_template('index.html', servers=uses_guilds, uses=uses,commands=commands, reviews=reviews)



def add_otziv(otziv):
  data = open_otzivi()
  if otziv.lower() in data or 'discord.gg' in otziv or 'discord.com' in otziv or 'http' in otziv:
    return
  data.append(otziv)
  with open('revies.json', 'w') as f:
    json.dump(data, f)

@app.route('/add_review', methods=['POST'])
@limiter.limit("5 per second")
def add_review():
    review = request.form['review']
    if len(review) > 0 and len(review) < 100:
      add_otziv(review)
    return "Nice"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
