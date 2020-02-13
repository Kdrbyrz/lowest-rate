### Run Command
`docker-compose up`

### Testing
You need to run this command  
`export FLASK_ENV=development`

###Integrating Provider
You have to edit providers.env file  
Each of provider must have 'url', 'code_key', 'rate_key'
`providers=[{"url": "http://www.mocky.io/v2/5d19ec932f00004e00fd7326","code_key": "code","rate_key": "rate"}]
`