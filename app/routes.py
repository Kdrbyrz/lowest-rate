from app import app


@app.route('/rate/<string:currency>/', methods=['GET'])
def lowest_rate(currency):
    return 'hello world'


@app.route('/daily/rate/<string:currency>/', methods=['GET'])
def daily_rate(currency):
    return 'hw2'
