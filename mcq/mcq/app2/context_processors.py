from account.models import User
from app.models import *

def user_info(request):
    user = request.user
    return {'user_info': user}


# def company(request):
#     user = AboutUS.objects.first()
#     return {'company': user}


from account.models  import User
# from orders.models import Order

from django.db.models import Sum
from django.db.models import Q
from datetime import datetime
# from accounting.models import Daily
# import nepali_datetime
# from dateutil.relativedelta import relativedelta
from datetime import date,timedelta

# from dashboard.models import AboutUS






def usercount(request):
    totalClient = User.objects.filter(is_user= True).count
    return ({
        'totalClient':totalClient
    })


def invoice(request):
    received_orders = Purchases.objects.filter(payment_status='paid')
    paid_amount = received_orders.aggregate(total_cost=Sum('paid_amount'))['total_cost'] or 0
    order = Purchases.objects.all().count
    set = QuestionSets.objects.all().count

    unreceived_orders = Purchases.objects.exclude(Q(payment_status='paid'))
    unpaid_amount = unreceived_orders.aggregate(total_cost=Sum('paid_amount'))['total_cost'] or 0


    return({
        'paidamount':paid_amount,
        'totalOrders':order,
        'unpaidamount':unpaid_amount,
        'set':set
    })
