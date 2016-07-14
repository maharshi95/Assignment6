from django.shortcuts import render
from django import http
from django.db import connection
from .models import Product,Orders,Orderdetails
import datetime
import json

query_former = "SELECT DATE(time_created) as order_date, SUM(OD.quantity) AS qty, COUNT(O.order_id) AS orders, " \
               "SUM(P.buy_price) AS buy_price, SUM(OD.sell_price) AS sell_price, SUM((OD.sell_price - P.buy_price) * OD.quantity) AS profit " \
               "FROM Orders AS O, OrderDetails AS OD, Product AS P " \
               "WHERE O.order_id = OD.order_id " \
               "AND OD.product_id = P.product_id " \
               "AND O.order_status != 'Cancelled' "

lower_bound = "AND time_created >= '%s' "

upper_bound = "AND time_created <= '%s' "

query_latter = "GROUP BY order_date " \
               "ORDER BY order_date " \
               "DESC"

date_fmt = '%m/%d/%Y'

def process_query(sdate_str,edate_str):
    start_date = (datetime.datetime.strptime(sdate_str, date_fmt) if (sdate_str is not None) else None)
    end_date = (datetime.datetime.strptime(edate_str, date_fmt) if (edate_str is not None) else None)

    query = query_former
    if start_date is not None:
        query += lower_bound.replace('%s',str(start_date))
    if end_date is not None:
        query += upper_bound.replace('%s', str(end_date))
    query += query_latter

    print("query: ", query)

    # result_set = Orderdetails.objects.raw(query)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [item for item in cursor.fetchall()]
    report = []
    for row in rows:
        per_day_sale = {
            'date': row[0].strftime(date_fmt),
            'orders': int(row[2]),
            'qty': int(row[1]),
            'buy_price': float(row[3]),
            'sell_price': float(row[4]),
            'profit': float(row[5])
        }
        report.append(per_day_sale)
    print(report)
    return report


def get_daily_sales(request):
    start_date = request.GET['startDate'] if 'startDate' in request.GET else None
    end_date = request.GET['endDate'] if 'endDate' in request.GET else None
    data = process_query(start_date,end_date)
    output = json.dumps({"data": data})
    output = json.dumps(json.loads(output), indent=4)
    return http.HttpResponse(output,content_type='application/json')
