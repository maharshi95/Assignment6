from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
import dateutil.parser as parser
from api import app_utils
import datetime
from dateutil import tz
import pytz

app = app_utils.create_app()

db = SQLAlchemy(app)

query_max_limit = 10
fmt = '%m/%d/%YT%H:%M:%S'

utc_tz = tz.gettz('UTC')
dubai_tz = tz.gettz('Asia/Dubai')

def date_utc(date_obj):
    local = date_obj.replace(tzinfo=dubai_tz)
    local = local.astimezone(utc_tz)
    return local.strftime(fmt)
    # local = pytz.timezone("Asia/Dubai")
    # naive = datetime.datetime.strptime(str(date_obj), "%Y-%m-%d %H:%M:%S")
    # local_dt = local.localize(naive, is_dst=None)
    # utc_dt = local_dt.astimezone(pytz.utc)
    # return utc_dt.strftime(fmt)

class AuditLog(db.Model):
    # __tablename__ = 'audit_log'
    audit_id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime)
    url = db.Column(db.String)
    params = db.Column(db.String)
    ip_address = db.Column(db.String)
    request_type = db.Column(db.String)
    request_duration_ms = db.Column(db.BigInteger)
    response_code = db.Column(db.BigInteger)

    def __init__(self, audit_id, time_created, url, params, ip_address, request_type, request_duration, response_code):
        self.audit_id = audit_id
        self.time_created = time_created
        self.url = url
        self.params = params
        self.ip_address = ip_address
        self.request_duration_ms = request_duration
        self.response_code = response_code
        self.request_type = request_type

    def __repr__(self):
        return str(('AuditLog' + str(self.audit_id),
                    self.time_created,
                    self.url,
                    self.ip_address,
                    self.request_type,
                    self.params,
                    self.request_duration_ms,
                    self.response_code))

    def to_json(self):
        return {
            "timestamp": date_utc(self.time_created),
            "url": self.url,
            "parameters": self.params,
            "request_ip_address": self.ip_address,
            "request_duration_ms": self.request_duration_ms,
            "request_type": self.request_type,
            "response_code": self.response_code,
        }


@app.route('/api/auditLogs')
def getLogs():
    print(datetime.datetime.now())
    lower_bound = request.args.get('startTime')
    upper_bound = request.args.get('endTime')
    print(lower_bound, upper_bound)
    page_size = request.args.get('limit')
    page_no = request.args.get('offset')
    query = AuditLog.query
    if lower_bound is not None:
        lower_bound = parser.parse(lower_bound)
        lower_bound = lower_bound.replace(tzinfo=utc_tz)
        lower_bound = lower_bound.astimezone(dubai_tz)
        print(lower_bound)
        query = query.filter(AuditLog.time_created >= lower_bound)
    if upper_bound is not None:
        upper_bound = parser.parse(upper_bound)
        upper_bound = upper_bound.replace(tzinfo=utc_tz)
        upper_bound = upper_bound.astimezone(dubai_tz)
        query = query.filter(AuditLog.time_created <= upper_bound)
    if page_no is None:
        page_no = 0
    if (page_size is None) or (int(page_size) > query_max_limit) or (int(page_size) <= 0):
        page_size = query_max_limit
    logs = query.order_by(AuditLog.time_created.desc()).limit(page_size).offset(page_no).all()
    jlist = []
    print(logs)
    for log in logs:
        obj = log.to_json()
        jlist.append(obj)
        print(obj)
    print("jlist:",jlist)
    response_body = {
        "data": jlist
    }
    return jsonify(response_body)

if __name__ == "__main__":
    app.run(debug=True)
