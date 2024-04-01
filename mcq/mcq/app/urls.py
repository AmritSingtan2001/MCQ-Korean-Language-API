from django.urls import path
from . import views
from . views import (CategoriesView,QuestionsView, PurchasesQuestionSets,SliderListAPIview,PurchaseCreateAPIView,ExamList,ScoreCreateAPIView,PaymentPatnerList,FreeQuestionList)

urlpatterns = [
    path('sliders', SliderListAPIview.as_view(), name='sliders'),
    path('category', CategoriesView.as_view(), name='categories'), #all category get
    path('category/<int:id>', CategoriesView.as_view(), name='categories'), # categorie related question sets
    path('questions_sets',QuestionsView.as_view(), name='questionsset'), # all question sets get
    path('questions_sets/<int:id>',QuestionsView.as_view(), name='questions'), # set related questions
    path('question_sets/purchase',PurchasesQuestionSets.as_view(), name='purchase_question_sets' ), #Purchase Question sets list
    path('question_sets/purchase/create', PurchaseCreateAPIView.as_view(), name='purchase_question_set'),
    path('exam',ExamList.as_view(), name ='examlist'),
    path('score',ScoreCreateAPIView.as_view(),name='score_create'),
    path('payment_method',PaymentPatnerList.as_view(), name='payment_method' ), # payment method
    path('free',FreeQuestionList.as_view(), name='free_question')


]