from flask import Flask

host = 'aline-cnu-insights-dev-cluster.cluster-czuocyoc6awe.us-east-1.rds.amazonaws.com'
port = 3306
user = 'mgor'
password = 'mgor'
db_name = 'cnu2016_mgor'
db_url = ('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db_name)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    return app
