from django.shortcuts import render,HttpResponse, HttpResponseRedirect,redirect,get_object_or_404
from django.views import View
from account.models import User
from django.contrib.auth import authenticate, login, logout
from . decorators import login_required
from django.contrib import messages
from django.contrib import auth
from . forms import *
from app.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
# from . new_file_handler import validate_file
# from django.http import JsonResponse
from django.http import HttpResponseBadRequest


def login(request):
    try:
        if request.user.is_authenticated:
            return render(request,'app2/index.html')
        if request.method =="POST":
            email = request.POST['useremail']
            print(email)
            password = request.POST['password']
            print(password)
            # user_obj = User.objects.filter(email=email)
            user_obj = authenticate(email=email, password=password)
            print(user_obj)
            if not user_obj: #not user_obj.exists():
                messages.warning(request,"Invalid username and password...")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(email=email, password=password)
            if user_obj and user_obj.is_admin or user_obj.is_editor:
                auth.login(request, user_obj)
                return redirect('dashboard:index')
            messages.warning(request,'Inavlid Password')
            return redirect('dashboard:login')
        return render(request,'app2/login.html')
    except Exception as e:
        print(e)
        messages.warning(request,'something wrong...')
        return redirect('dashboard:login')

@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')


@login_required
def index(request):
    return render(request,'app2/index.html')



 
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user)  # Important to update the session after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:change_password')  # Redirect to the same view after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'app2/change_password.html', {'form': form})






@login_required
def add_edit_Categories(request, id=None):
    instance = None
    related_sets=None
    try:
        if id:
            instance = Categories.objects.get(pk=id)
            related_sets = QuestionSets.objects.filter(categorie= instance)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the Categories.')
        return redirect('dashboard:add_Categories')

    if request.method == 'POST':
        form = CategoriesForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Categories edited successfully.')
                return redirect('dashboard:edit_Categories', id=instance.id)  # Redirect to the edited Categories's details page
            else:  # Add operation
                messages.success(request, 'Categories added successfully.')
                return redirect('dashboard:add_Categories')  # Redirect to the page for adding new Categoriess
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = CategoriesForm(instance=instance)

    context = {'form': form, 'instance': instance, 'related_sets':related_sets}
    return render(request, 'app2/create_Categories.html', context)


@login_required
def categorie(request):
    categorie=Categories.objects.all()
    p=Paginator(categorie,10)
    page_number= request.GET.get('page')
    categorie=p.get_page(page_number)
    return render(request, 'app2/categorie.html',{'details':categorie})


def category_related_sets(request, slug):
    return render(request,'app2/allquestionsets.html')

@login_required
def deleteCategories(request, id):
    
    if request.method == 'POST':
        record = get_object_or_404(Categories, id=id)
        try:
            record.delete()
            messages.success(request, "Deleted successfully!")
        except models.ProtectedError as e:
            error_message = str(e.args[0])  # Extract the error message from the tuple
            print(error_message)
            messages.warning(request, f"An error occurred: {error_message}")
        return redirect('dashboard:categorie')  # Redirect to a list view after deletion

    return render(request, 'app2/categorie.html', {'details': record})



@login_required
def score(request):
    categorie=Score.objects.all()
    p=Paginator(categorie,10)
    page_number= request.GET.get('page')
    categorie=p.get_page(page_number)
    return render(request, 'app2/Score.html',{'details':categorie})


@login_required
def deleteScore(request, id):
    
    if request.method == 'POST':
        record = get_object_or_404(Score, id=id)
        try:
            record.delete()
            messages.success(request, "Deleted successfully!")
        except models.ProtectedError as e:
            error_message = str(e.args[0])  # Extract the error message from the tuple
            print(error_message)
            messages.warning(request, f"An error occurred: {error_message}")
        return redirect('dashboard:Score')  # Redirect to a list view after deletion

    return render(request, 'app2/Score.html', {'details': record})




@login_required
def purchase_list(request):
    orders= Purchases.objects.all()
    return render(request,'app2/purchases.html',{'details':orders})

@login_required
def update_purchase_list(request,id):
    orders = get_object_or_404(Purchases, id=id)

    if request.method=="POST":
        id= request.POST['id']
        print(id)
        orders.payment_status= request.POST['payment_status']
        print(request.POST['payment_status'])
        orders.save()
        # messages.info(request,'Update successfully !')
        return redirect('dashboard:purchases')
    return redirect('dashboard:purchases')


@login_required
def deletepurchases(request, id):
    record = get_object_or_404(Purchases, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:purchases')  # Redirect to a list view after deletion

    return render(request, 'app2/purchases.html', {'details': record})


@login_required
def question(request, id):
    questionset = get_object_or_404(QuestionSets, id=id)
    questions = Questions.objects.filter(set_name=questionset)
    main_form = QuestionsForm()
    answer_forms = AnswerForm()
    return render(request, 'app2/questions.html', {'questions': questions, 'questionset': questionset,'form': main_form, 'answer_forms': answer_forms, 'loop_times': range(4)})



@login_required
def add_edit_QuestionSets(request, id=None):
    instance = None
  
    try:
        if id:
            instance = QuestionSets.objects.get(pk=id)
            
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the QuestionSets.')
        return redirect('dashboard:add_QuestionSets')

    if request.method == 'POST':
        form = QuestionSetsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'QuestionSets edited successfully.')
                return redirect('dashboard:edit_QuestionSets', id=instance.id)  # Redirect to the edited QuestionSets's details page
            else:  # Add operation
                messages.success(request, 'QuestionSets added successfully.')
                return redirect('dashboard:add_QuestionSets')  # Redirect to the page for adding new QuestionSetss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = QuestionSetsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_QuestionSets.html', context)



@login_required
def questionSets(request):
    questionSets=QuestionSets.objects.all()
    p=Paginator(questionSets,12)
    page_number= request.GET.get('page')
    questionSets=p.get_page(page_number)
    return render(request, 'app2/questionSets.html',{'details':questionSets})



@login_required
def collection(request):
    categorie=Categories.objects.all()
    p=Paginator(categorie,12)
    page_number= request.GET.get('page')
    categorie=p.get_page(page_number)
    return render(request, 'app2/Collection.html',{'details':categorie})



@login_required
def add_edit_Collection(request, id=None):
    instance = None
    related_sets=None
    try:
        if id:
            instance = Categories.objects.get(pk=id)
            related_sets = QuestionSets.objects.filter(categorie= instance)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the Categories.')
        return redirect('dashboard:add_Categories')

    if request.method == 'POST':
        form = CategoriesForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Categories edited successfully.')
                return redirect('dashboard:edit_Categories', id=instance.id)  # Redirect to the edited Categories's details page
            else:  # Add operation
                messages.success(request, 'Categories added successfully.')
                return redirect('dashboard:add_Categories')  # Redirect to the page for adding new Categoriess
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = CategoriesForm(instance=instance)

    context = {'form': form, 'instance': instance, 'related_sets':related_sets}
    return render(request, 'app2/create_Collection.html', context)

# def collection(request):
#     questionSets=Categories.objects.all()
#     p=Paginator(questionSets,12)
#     page_number= request.GET.get('page')
#     questionSets=p.get_page(page_number)
#     return render(request, 'app2/Collection.html',{'details':questionSets})

@login_required
def deletequestionSets(request, id):
    record = get_object_or_404(QuestionSets, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:questionSets')  # Redirect to a list view after deletion

    return render(request, 'app2/questionSets.html', {'details': record})


def load_sub_category(request):
    main_ctg_id = request.GET.get('programming')
    sub_category = QuestionSets.objects.filter(categorie=main_ctg_id)
    return render(request,'app2/listdropdow.html',{'sub_category':sub_category})

from django.shortcuts import render, redirect

from django.http import JsonResponse

# Add Mutiple question and answer 


class AddQuestionView(View):
    template_name = 'app2/create_Questions.html'  # Change this to the path of your template

    def get(self, request, *args, **kwargs):
        form = QuestionsForm()  # Replace QuestionsForm with the actual form you're using
        categories = Categories.objects.all()
        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request, *args, **kwargs):
        form = QuestionsForm(request.POST, request.FILES)  # Replace YourForm with the actual form you're using
        if form.is_valid():
            # Save the form data and handle dependencies
            question_set = form.save(commit=False)
            question_set.categorie = form.cleaned_data['categorie']
            question_set.save()
            return redirect('your_redirect_url')  # Replace with the URL you want to redirect to
        else:
            categories = Categories.objects.all()
            print(form.categorie)
            return render(request, self.template_name, {'form': form, 'categories': categories})


  
class GetQuestionSetsView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        question_sets = QuestionSets.objects.filter(categorie_id=category_id)
        data = [{'id': qs.id, 'set_name': qs.set_name} for qs in question_sets]
        return JsonResponse(data, safe=False)


@login_required
def add_edit_Slider(request, id=None):
    instance = None
    try:
        if id:
            instance = Slider.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the Slider.')
        return redirect('dashboard:add_Slider')

    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Slider edited successfully.')
                return redirect('dashboard:edit_Slider', id=instance.id)  # Redirect to the edited Slider's details page
            else:  # Add operation
                messages.success(request, 'Slider added successfully.')
                return redirect('dashboard:add_Slider')  # Redirect to the page for adding new Sliders
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = SliderForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_slider.html', context)


@login_required
def slider(request):
    slider=Slider.objects.all()
    p=Paginator(slider,10)
    page_number= request.GET.get('page')
    slider=p.get_page(page_number)
    return render(request, 'app2/slider.html',{'details':slider})

@login_required
def deleteSlider(request, id):
    record = get_object_or_404(Slider, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:slider')  # Redirect to a list view after deletion

    return render(request, 'app2/slider.html', {'details': record})





# Question add with mutiple 
# views.py
from django.shortcuts import render, redirect
from .forms import QuestionSetsForm, QuestionsForm, AnswerForm

@login_required
def add_question_set(request):
    if request.method == 'POST':
        question_set_form = QuestionSetsForm(request.POST)
        question_form = QuestionsForm(request.POST, request.FILES)
        answer_form = AnswerForm(request.POST, request.FILES)

        if question_set_form.is_valid() and question_form.is_valid() and answer_form.is_valid():
            question_set_instance = question_set_form.save()

            question_instance = question_form.save(commit=False)
            question_instance.set_name = question_set_instance
            question_instance.save()

            answer_instance = answer_form.save(commit=False)
            answer_instance.question = question_instance
            answer_instance.save()

            return HttpResponse('success_page')  # Redirect to a success page

    else:
        question_set_form = QuestionSetsForm()
        question_form = QuestionsForm()
        answer_form = AnswerForm()

    return render(request, 'app2/test.html', {'question_set_form': question_set_form, 'question_form': question_form, 'answer_form': answer_form})



# testing 
# views.py
from django.shortcuts import render, redirect
from .forms import QuestionSetsForm, QuestionsForm, AnswerForm

# @login_required
# def add_question(request, setid=None):
#     if request.method == "POST":
#         main_form = QuestionsForm(request.POST, request.FILES)
#         if main_form.is_valid():
#             main_instance = main_form.save()
            
#             additional_fields = {}
            
#             for key, value in request.POST.items():
#                 if key.startswith(('answer', 'answerfile', 'correct')):
#                     field_type, *rest = key.split('_')
#                     index = rest[0] if rest else '0'
                    
            
#                     if field_type == 'correct' and value == 'on':
#                         value = True
#                     elif field_type == 'correct' and value != 'on':
#                         value = False

                        
#                     additional_fields.setdefault(int(index), {})[field_type] = value


#             for key, file in request.FILES.items():
#                 if key.startswith('answerfile'):
#                     field_type, *rest = key.split('_')
#                     index = rest[0] if rest else '0'
#                     additional_fields.setdefault(int(index), {})[field_type] = file

            

#             for index, fields in additional_fields.items():
#                     print("aAA:", fields)
 
#                     fields['question'] = main_instance 
#                     Answer.objects.create(**fields)
            
#             return redirect('dashboard:addquestion', main_instance.set_name.id)
    
#         else:
#             return JsonResponse({'success': False, 'errors': main_form.errors}, status=400)
#     else:
#         main_form = QuestionsForm()
#         answer_forms = AnswerForm()
#         return render(request, 'app2/test.html', {'form': main_form, 'answer_forms': answer_forms, 'loop_times': range(4),'set_name':setid})
    

# from django.utils.encoding import smart_text
# update and add question 
from django.shortcuts import get_object_or_404


# thisis it
@login_required
def add_question(request, setid=None, question_id=None):
    if question_id:
        question_instance = get_object_or_404(Questions, id=question_id)
        main_form = QuestionsForm(request.POST or None, request.FILES or None, instance=question_instance)
        question_instance.answers.all().delete()
    else:
        main_form = QuestionsForm(request.POST or None, request.FILES or None)
        
        

    answer_forms = AnswerForm()

    if request.method == "POST":
        if main_form.is_valid():
            main_instance = main_form.save()
          

            additional_fields = {}
            
         
            for key, value in request.POST.items():
                if key.startswith(('answer', 'audio', 'image', 'correct')) and key[-1].isdigit():
                    try:
                        field_type, index = key.rsplit('_', 1)
                        index = int(index) 
                    except ValueError as e:
                        continue 

                    if field_type == 'correct':
                        value = (value == 'on')

                    additional_fields.setdefault(index, {})[field_type] = value

            for key, file in request.FILES.items():
                if key.startswith(('audio', 'image')) and key[-1].isdigit():
                    field_type, index = key.rsplit('_', 1)
                    additional_fields.setdefault(int(index), {})[field_type] = file

            update_status = False
            for index, fields in additional_fields.items():
                fields['question'] = main_instance
                answer_id = request.POST.get(f'id_{index}')
                if answer_id:
                    if 'correct' not in fields:
                        fields['correct'] = False

                    if 'image' not in fields and request.FILES.get(f'image_{index}'):
                        fields['image'] = request.FILES.get(f'image_{index}')
                    if 'audio' not in fields and request.FILES.get(f'audio_{index}'):
                        fields['audio'] = request.FILES.get(f'audio_{index}')

                    Answer.objects.filter(id=answer_id).update(**fields)
                    update_status = True
                else:
                    Answer.objects.create(**fields)

            if update_status:
                messages.success(request, "Update Successfully !")
                return redirect('dashboard:question', main_instance.set_name.id)
            else:
                messages.success(request, 'New Question added Successfully !')
                return redirect('dashboard:addquestion', main_instance.set_name.id)
        else:
            return JsonResponse({'success': False, 'errors':main_form.errors}, status=400)

    return render(request, 'app2/test.html', {'form': main_form, 'answer_forms': answer_forms, 'loop_times': range(4), 'set_name': setid})




# delete question
@login_required
def question_delete(request):
    instance=None
    if request.method =="POST":
        questionId = request.POST.get('questionID')
        instance = Questions.objects.get(id=questionId)
        messages.success(request,f"Question deleted Successfully !")
        instance.delete()
        return redirect("dashboard:question", instance.set_name.id)
    else:
        return redirect("dashboard:question", instance.set_name.id)


@login_required
def user(request):
    user = User.objects.filter(is_user=True)
    return render(request, 'app2/user.html', {'user': user})



@login_required
def deletequestionset(request, id):
    record = get_object_or_404(QuestionSets, id=id)

    if request.method == 'POST':
        record.delete()
        messages.success(request,'Question set deleted successfully !')
        return redirect('dashboard:questionSets')  # Redirect to a list view after deletion

    return render(request, 'app2/questionSets.html', {'details': record})





# # question id related data
import os
# def get_question_details(request):
#     question_id = request.GET.get('question_id')
    
#     try:
#         question = Questions.objects.get(id=question_id)
#         answers = list(Answer.objects.filter(question=question).values())
        
#         answer_data = []
#         for answer in answers:
#             answer_file = answer.get('answerfile')
#             file_name = os.path.basename(answer_file) if answer_file else "None"

#             answer_data.append({
#                 'id':answer.get('id'),
#                 'answer': answer.get('answer'),
#                 'answerfile': file_name,
#                 'correct': answer.get('correct'),
#             })

#         data = {
#             'id': question.id,
#             'set_name':question.set_name.id,
#             'question': question.question,
#             'file':os.path.basename(question.file.url) if answer_file else "None" ,
#             'answer':answer_data,
            
#         }
#         return JsonResponse(data,safe=False)
#     except Questions.DoesNotExist:
#         return JsonResponse({'error': 'Question not found'}, status=404)



def get_question_details(request):
    question_id = request.GET.get('question_id')

    try:
        question = Questions.objects.get(id=question_id)
        answers = list(Answer.objects.filter(question=question).values())

        answer_data = []
        for answer in answers:
            answer_file = answer.get('audio') or answer.get('image')
            file_name = os.path.basename(answer_file) if answer_file else "None"

            answer_data.append({
                'id': answer.get('id'),
                'answer': answer.get('answer'),
                'answerfile': file_name,
                'correct': answer.get('correct'),
            })

        data = {
            'id': question.id,
            'set_name': question.set_name.id,
            'question': question.question,
            'file': os.path.basename(question.audio.url) if question.audio else "None",
            'image': os.path.basename(question.image.url) if question.image else "None",
            'answer': answer_data,
        }
        return JsonResponse(data, safe=False)
    except Questions.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)





@login_required
def create_question(request, question_id=None):
    # If question_id is provided, it's an edit operation; otherwise, it's a new creation
    question_set=QuestionSets.objects.all()
    if question_id:
        question_instance = get_object_or_404(Questions, id=question_id)
    else:
        # Create a new Questions instance
        question_instance = Questions()

    # Create an inline formset for Answer
    AnswerFormSet = inlineformset_factory(Questions, Answer, form=AnswerForm, extra=0)

    if request.method == 'POST':
        question_form = QuestionsForm(request.POST, request.FILES, instance=question_instance)
        formset = AnswerFormSet(request.POST, request.FILES, instance=question_instance)

        if question_form.is_valid() and formset.is_valid():
            print("Form is valid.")

            # Save the question instance
            question_form.save()

            # Save the formset (answers)
            formset.save()

            # If it's an edit, redirect to the same editing page
            if question_id:
                messages.success(request, 'Update Question and Answer  successfully.')


                return redirect('dashboard:edit_question', question_id=question_instance.id)

            # If it's a new creation, redirect to the new Questions's editing page
            return redirect('dashboard:edit_question', question_id=question_instance.id)

        else:
            print("Form is not valid:", question_form.errors, formset.errors)
    else:
        question_form = QuestionsForm(instance=question_instance)
        formset = AnswerFormSet(instance=question_instance)

    context = {
        'question_form': question_form,
        'formset': formset,
        'is_inline_formset_used': True,
        'question_set':question_set
    }

    return render(request, 'app2/edit_questions.html', context)
# def create_question(request, question_id=None):
#     # If question_id is provided, it's an edit operation; otherwise, it's a new creation
#     if question_id:
#         question_instance = get_object_or_404(Questions, id=question_id)
#     else:
#         # Create a new Questions instance
#         question_instance = Questions.objects.create()

#     # Create an inline formset for Answer
#     AnswerFormSet = inlineformset_factory(Questions, Answer, form=AnswerForm, extra=1)

#     if request.method == 'POST':
#         question_form = QuestionsForm(request.POST, instance=question_instance)
#         formset = AnswerFormSet(request.POST, instance=question_instance)

#         if question_form.is_valid() and formset.is_valid():
#             question_form.save()
#             formset.save()

#             # If it's an edit, redirect to the same editing page
#             if question_id:
#                 return redirect('dashboard:edit_question', question_id=question_instance.id)

#             # If it's a new creation, redirect to the new Questions's editing page
#             return redirect('dashboard:edit_question', question_id=question_instance.id)

#     else:
#         question_form = QuestionsForm(instance=question_instance)
#         formset = AnswerFormSet(instance=question_instance)

#     context = {
#         'question_form': question_form,
#         'formset': formset,
#         'is_inline_formset_used': True,
#     }

#     return render(request, 'app2/questions1.html', context)
# def create_question_set(request, question_set_id=None):
#     if question_set_id:
#         question_set_instance = get_object_or_404(QuestionSets, id=question_set_id)
#     else:
#         question_set_instance = QuestionSets.objects.create()

#     QuestionsFormSet = inlineformset_factory(QuestionSets, Questions, form=QuestionsForm, extra=1)
#     AnswerFormSet = inlineformset_factory(Questions, Answer, form=AnswerForm, extra=1)

#     if request.method == 'POST':
#         question_set_form = QuestionSetsForm(request.POST, instance=question_set_instance)
#         questions_formset = QuestionsFormSet(request.POST, instance=question_set_instance)
#         answer_formset = AnswerFormSet(request.POST, instance=question_set_instance)

#         if question_set_form.is_valid() and questions_formset.is_valid() and answer_formset.is_valid():
#             question_set_form.save()
#             questions_formset.save()
#             answer_formset.save()

#             if question_set_id:
#                 return redirect('dashboard:edit_question_set', question_set_id=question_set_instance.id)
            
#             return redirect('dashboard:edit_question_set', question_set_id=question_set_instance.id)

#     else:
#         question_set_form = QuestionSetsForm(instance=question_set_instance)
#         questions_formset = QuestionsFormSet(instance=question_set_instance)
#         answer_formset = AnswerFormSet(instance=question_set_instance)

#     context = {
#         'question_set_form': question_set_form,
#         'questions_formset': questions_formset,
#         'answer_formset': answer_formset,
#         'is_inline_formset_used': True,
#     }

#     return render(request, 'app2/questions1.html', context)



#news subcategorie
def add_edit_Group(request, id=None):
    instance = None
    try:
        if id:
            instance = Group.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Group.')
        return redirect('dashboard:add_Group')
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Group edited successfully.')
                return redirect('dashboard:edit_Group', id=instance.id)  # Redirect to the edited Group's details page
            else:  # Add operation
                messages.success(request, 'Group added successfully.')
                return redirect('dashboard:add_Group')  # Redirect to the page for adding new Groups
        else:
            messages.warning(request, form.errors)
    else:
        form = GroupForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_Group.html', context)
def Groups(request):
    Groups=Group.objects.all()
    p=Paginator(Groups,4)
    page_number= request.GET.get('page')
    Groups=p.get_page(page_number)
    return render(request, 'app2/Group.html',{'details':Groups})
# @user_role_required('admin')
def deleteGroup(request, id):
    record = Group.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:Group')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/Group.html', {'details': record})