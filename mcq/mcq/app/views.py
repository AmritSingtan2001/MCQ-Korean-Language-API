from django.shortcuts import render, HttpResponse
from . models import Categories, Questions, QuestionSets, Answer, Purchases,Slider,Score,PaymentPatner
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CategoriesSerailizers,QuestionSetSerializers,QuestionSerializer,SliderSerializers,PurchaseSerializer,ScoreSerializer,PaymentPatnerSerailizer



# Slider List 
class SliderListAPIview(generics.ListAPIView):
    serializer_class = SliderSerializers

    def get_queryset(self):
        return Slider.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except serializer.ValidationError as e:
            return Response({'message': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoriesView(generics.ListAPIView):
    queryset = Categories.objects.all().order_by('order_number')
    serializer_class = CategoriesSerailizers

    def list(self, request, *args, **kwargs):
        if 'id' in kwargs:
            category = Categories.objects.get(id=kwargs['id'])
            print(category)
            question_sets_queryset = QuestionSets.objects.filter(categorie=category)
            print(question_sets_queryset)
            category_serializer = CategoriesSerailizers(category)
            question_sets_serializer = QuestionSetSerializers(question_sets_queryset, many=True)
            
            response_data = {
                "category": category_serializer.data,
                "question_sets": question_sets_serializer.data,
                "success": True
            }
        else:
            queryset = self.get_queryset()
            serializer = CategoriesSerailizers(queryset, many=True)
            response_data = {
                "data": serializer.data,
                "success": True
            }

        return Response(response_data, status=status.HTTP_200_OK)
    




class QuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        if 'id' in self.kwargs:
            print(self.kwargs['id'])
            question_set = QuestionSets.objects.get(id=self.kwargs['id'])
            print(question_set)
            return Questions.objects.filter(set_name=question_set)
        else:
            return Questions.objects.all()


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "data": serializer.data,
            "success": True
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

# user purchase question sets list 
class PurchasesQuestionSets(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_authenticated:
            has_purchases = Purchases.objects.filter(user=user, payment_status="paid").exists()
            print(has_purchases)
            if has_purchases:
                purchased_categories = Purchases.objects.filter(user=user, payment_status="paid").values_list('sets', flat=True).distinct()

                purchase_categories = Categories.objects.filter(id__in=purchased_categories)

                question_sets_instances = QuestionSets.objects.filter(categorie__in=purchase_categories)
                question_sets_serializer = QuestionSetSerializers(question_sets_instances, many=True)


                response_data = {
                    "question_sets": question_sets_serializer.data,
                    "success": True
                }
                return Response({'data': response_data}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'No Question Banks Purchased yet!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Login first'}, status=status.HTTP_401_UNAUTHORIZED)


# Question sets Purchase Request
class PurchaseCreateAPIView(generics.CreateAPIView):
    queryset = Purchases.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, payment_status='pending')

    def create(self, request, *args, **kwargs):
        user = self.request.user
        set_id = request.data.get('sets')
        
        if Purchases.objects.filter(user=user, sets_id=set_id, payment_status="pending").exists():
            set_name = QuestionSets.objects.get(id=set_id).set_name
            return Response({'set_name':set_name,'message': f'You have already requested to purchase the set "{set_name}" but it is still pending.'}, status=status.HTTP_400_BAD_REQUEST)

        elif Purchases.objects.filter(user=user, sets_id=set_id, payment_status="paid").exists():
            set_name = QuestionSets.objects.get(id=set_id).set_name
            return Response({'set_name':set_name,'message': f'You have already purchased the set "{set_name}"!'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Your request to purchase this set has been sent successfully!'
        response.status_code =status.HTTP_201_CREATED
        return response

# Exams 
from django.db.models import Q
class ExamList(generics.ListAPIView):
    serializer_class = QuestionSetSerializers
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            has_purchases = Purchases.objects.filter(user=user, payment_status="paid").exists()
          
            if has_purchases:
                user_purchase_sets = Purchases.objects.filter(user=user, payment_status="paid")
                purchased_question_sets = user_purchase_sets.values_list('sets', flat=True).distinct()
                question_sets_instances = QuestionSets.objects.filter(
                    Q(id__in=purchased_question_sets) | Q(is_free=True)
                )
                question_sets_serializer = QuestionSetSerializers(question_sets_instances, many=True)
                response_data = {
                    "question_sets": question_sets_serializer.data,
                    "success": True
                }
                return Response({'data': response_data}, status=status.HTTP_200_OK)
            else:
                questionsets = QuestionSets.objects.filter(is_free = True)
                serializer = QuestionSetSerializers(questionsets, many=True)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Login first'}, status=status.HTTP_401_UNAUTHORIZED)


            
            

# score record
class ScoreCreateAPIView(generics.CreateAPIView):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Score Added Successfully !'
        response.status_code =status.HTTP_201_CREATED
        return response
        
        
# qr code 
class PaymentPatnerList(generics.ListAPIView):
    serializer_class = PaymentPatnerSerailizer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return PaymentPatner.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except serializer.ValidationError as e:
            return Response({'message': 'Validation error'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# free question
class FreeQuestionList(generics.ListAPIView):
    serializer_class = QuestionSetSerializers
    def list(self, request, *args, **kwargs):
        questionsets = QuestionSets.objects.filter(is_free = True)
        serializer = QuestionSetSerializers(questionsets, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)



