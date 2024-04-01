from django.contrib import admin
from . models import *

class SliderAdmin(admin.ModelAdmin):
    model =Slider
    list_display=['id','text','image','order_number']
admin.site.register(Slider,SliderAdmin)


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display =['id','title']
admin.site.register(Group, GroupAdmin)

class PurchasesAdmin(admin.ModelAdmin):
    model =Purchases
    list_display =['user','sets','payment_method','payment_slip','paid_amount','payment_status']
    list_editable =['payment_status']
admin.site.register(Purchases,PurchasesAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    model = Categories
    list_display =['categories_name','previous_price','current_price','short_descriptions','image','order_number']
admin.site.register(Categories, CategoriesAdmin)


class QuestionSetsAdmin(admin.ModelAdmin):
    model = QuestionSets
    list_display =['set_name','id','categorie','is_free','order_number']
admin.site.register(QuestionSets, QuestionSetsAdmin)


class AnswerAdmin(admin.TabularInline):
    model = Answer
    max_num =4

class QuestionAdmin(admin.ModelAdmin):
    inlines =[AnswerAdmin]
admin.site.register(Questions, QuestionAdmin)



class ScoreAdmin(admin.ModelAdmin):
    model =Score
    list_display =['user','marks','attempt_date']
admin.site.register(Score, ScoreAdmin)


admin.site.register(PaymentPatner)


