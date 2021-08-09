# from .forms import SearchWordForm, EnglishWordForm, OshindongaWordForm, WordDefinitionForm, DefinitionExampleForm
# import sys
# from django.contrib.auth.models import User
# from dictionary.models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom

# TEST SEARCH FUNCTIONS
# context = {'form': '', 'searched_word': '',
#            'definitions': '', 'examples': ''}


# def search_examples(request, definitions_pks):
#     '''
#         Takes in a list of pks of found definitions and search if examples exist and return example objects.
#     '''
#     example_querysets = []
#     for definition_pk in definitions_pks:
#         example_queryset = DefinitionExample.objects.filter(
#             definition_id=definition_pk)
#         # If no definition found, an empty queryset is appended
#         example_querysets.append(example_queryset)
#     # print(example_querysets)
#     # print(len(example_querysets))
#     example_objects = []
#     no_example_found = 'No example found'
#     for example_queryset in example_querysets:
#         if len(example_queryset) > 0:  # If it's not an empty querset
#             # Loop through the queryset to extract objects
#             for i in range(len(example_queryset)):
#                 example_objects.append(example_queryset[i])
#         else:
#             example_objects.append(no_example_found)
#     context['examples'] = example_objects
#     # print('Example objects: %s' % example_objects)
#     return render(request, 'dictionary/search.html', context)


# def search_definitions(request, word_pairs_pks):
#     '''
#         Takes in a list pks of word pairs and return a list of pks of all definitions found.
#     '''
#     sub_request3 = request
#     definition_querysets = []
#     for pair_pk in word_pairs_pks:
#         definition_queryset = WordDefinition.objects.filter(
#             word_pair_id=pair_pk)
#         # If no definition found, an empty queryset is appended
#         definition_querysets.append(definition_queryset)
#     # print(definition_querysets)
#     # print(len(definition_querysets))
#     definition_objects = []
#     no_definition_found = 'No definition found'
#     for definition_queryset in definition_querysets:
#         if len(definition_queryset) > 0:  # If it's not an empty queryset
#             for i in range(len(definition_queryset)):
#                 definition_objects.append(definition_queryset[i])
#         else:
#             definition_objects.append(no_definition_found)
#     context['definitions'] = definition_objects
#     # print('Cleaned definitions: %s' % definition_objects)
#     definitions_pks = []
#     for i in range(len(definition_objects)):
#         if definition_objects[i] != no_definition_found:
#             definitions_pks.append(definition_objects[i].id)
#     # print(definitions_pks)
#     # return definitions_pks
#     search_examples(sub_request3, definitions_pks)


# def search_word_pairs(request, eng_word_pk):
#     '''
#         Using the English word pk (foreignkey id) search if for English|Oshindonga pairs and return a list of pks of all pair objects found.
#     '''
#     sub_request2 = request
#     # Return a queryset of all word pairs with the searched word
#     word_pairs = OshindongaWord.objects.filter(english_word_id=eng_word_pk)
#     print('Word_pairs1: %s' % word_pairs)
#     print(len(word_pairs))
#     if len(word_pairs) == 0:
#         print('Word_pairs2: %s' % word_pairs)
#         context['searched_word'] = [
#             'The word you searched is not yet translated into Oshindonga.']
#         return render(request, 'dictionary/search.html', context)
#     else:
#         context['searched_word'] = word_pairs
#         # Etract pk/id of each pair and save them in a list
#         word_pairs_pks = [
#             word_pair.id for word_pair in word_pairs]
#         # return word_pairs_pks
#         search_definitions(sub_request2, word_pairs_pks)


# def search_word(request):
#     '''
#         Check if the searched English word exists in the English model. If found return its pk
#     '''
#     sub_request = request
#     # print('Started here')
#     # Reset context variables when visiting for the first time or refreshing the page
#     # context['form'] = SearchWordForm()
#     context['searched_word'] = ''
#     context['definitions'] = ''
#     context['examples'] = ''
#     form = SearchWordForm(request.GET)
#     context['form'] = form
#     # print(form)
#     # print(form.is_valid())
#     if form.is_valid():
#         # print('Passed here')
#         word = form.cleaned_data['search_word']
#         try:
#             # Search within English model, and if foud:
#             eng_word = EnglishWord.objects.get(word=word)
#             # Get the the id/pk of the word found to be used in Oshindonga model
#             eng_word_pk = eng_word.id
#         except EnglishWord.DoesNotExist:
#             return render(request, 'dictionary/search.html', context)
#         search_word_pairs(sub_request, eng_word_pk)
#         return render(request, 'dictionary/search.html', context)
#     else:
#         return render(request, 'dictionary/search.html', context)

# app_name = 'dictionary'
# urlpatterns = [
#     path('', views.index, name="index"),
#     path('search/', views.search_word, name='search'),
#     path('add_english', views.add_english, name='add-english'),
#     path('add_oshindonga', views.add_oshindonga, name='add-oshindonga'),
#     path('add_definition', views.add_definition, name='add-definition'),
#     path('add_example', views.add_example, name='add-example'),
#     path('thankyou', views.thankyou, name='thankyou'),
#     path('english-word/<int:pk>/update/',
#          views.EnglishWordUpdate.as_view(), name='english-word-update'),
#     path('oshindonga-word/<int:pk>/update/',
#          views.OshindongaWordUpdate.as_view(), name='oshindonga-word-update'),
#     path('definition/<int:pk>/update/',
#          views.WordDefinitionUpdate.as_view(), name='word-definition-update'),
#     path('example/<int:pk>/update/', views.DefinitionExampleUpdate.as_view(),
#          name='definition-example-update'),
# ]

#     path('english', views.add_english, name='add-english'),
#     path('oshindonga', views.add_oshindonga, name='add-oshindonga'),
#     path('definition', views.add_definition, name='add-definition'),
#     path('example', views.add_example, name='add-example'),

#     {% url 'dictionary:english' %}


# def add_english(request):
#     if request.method == 'POST':
#         form = EnglishWordForm(request.POST)
#         if form.is_valid():
#             new_word = form
#             new_word.save()
#             return HttpResponseRedirect(reverse('dictionary:add-english'))
#     else:
#         form = EnglishWordForm()
#     return render(request, 'dictionary/add_english.html/', {'form': form, 'operation': 'Add new English word'})


# def add_oshindonga(request):
#     if request.method == 'POST':
#         form = OshindongaWordForm(request.POST)
#         if form.is_valid():
#             new_word = form
#             new_word.save()
#             return HttpResponseRedirect(reverse('dictionary:add-oshindonga'))
#     else:
#         form = OshindongaWordForm()
#     return render(request, 'dictionary/add_oshindonga.html/', {'form': form})


# def add_definition(request):
#     if request.method == 'POST':
#         form = WordDefinitionForm(request.POST)
#         if form.is_valid():
#             new_definition = form
#             new_definition.save()
#             return HttpResponseRedirect(reverse('dictionary:add-definition'))
#     else:
#         form = WordDefinitionForm()
#     return render(request, 'dictionary/add_definition.html/', {'form': form})


# def add_example(request):
#     if request.method == 'POST':
#         form = DefinitionExampleForm(request.POST)
#         if form.is_valid():
#             new_definition = form
#             new_definition.save()
#             return HttpResponseRedirect(reverse('dictionary:add_example'))
#     else:
#         form = DefinitionExampleForm()
#     return render(request, 'dictionary/add_example.html/', {'form': form})

#     {% elif example_object == 'No example found' %}
#       <li><i>Inapu monika oshiholelwa</i></li>

# class HistoryRecord():
#     '''Queries the history model of the datatbase and returns query sets of each model
#     '''

#     def __init__(self):
#         # A queryset of all history entries from EnglishWord (historicalenglishword) database
#         self.english = []
#         # A queryset of all history entries from OshindongaWord (historicaloshindongaword) database
#         self.oshindonga = []
#         # A queryset of all history entries from WordDefinition (historicalenglisworddefinition) database
#         self.definition = []
#         # A queryset of all history entries from DefinitionExample (historicaldefinitionexample) database
#         self.example = []
#         # A queryset of all history entries from OshindongaIdiom (historicalenglishwordoshindongaidiom) database
#         self.idiom = []
#         self.usernames = []  # Holds all usernames from all history entries
#         self.unique_usernames = set()  # Holds unique usernames (set) from the usernames list

#     def reset_history(self):
#         self.english = []
#         self.oshindonga = []
#         self.definition = []
#         self.example = []
#         self.idiom = []
#         self.usernames = []
#         self.unique_usernames = set()
#         return

#     def english_history(self):
#         # Holds user ids of historical_users (created/modifiers)
#         self.english = EnglishWord.history.all()
#         self.user_ids = []
#         for queryset in self.english:  # Loops through the querysets and take the user id if it's not null/none
#             if queryset.history_user_id != None:  # Appends the the user id to user_ids list
#                 self.user_ids.append(queryset.history_user_id)
#         for user_id in self.user_ids:  # Loops through user ids and matches them to users to obtain usernames
#             # Holds querysets of users from the User model
#             user = User.objects.get(id=user_id)
#             # Appends the username to the usernames list
#             self.usernames.append(user.username)
#         # Updates the unique_usernames set with usernames
#         self.unique_usernames.update(self.usernames)
#         return self.english  # Returns a a queryset of EnglishWord historical objects/records

#     def oshindonga_history(self):
#         self.oshindonga = OshindongaWord.history.all()
#         self.user_ids = []
#         for queryset in self.oshindonga:
#             if queryset.history_user_id != None:
#                 self.user_ids.append(queryset.history_user_id)
#         for user_id in self.user_ids:
#             user = User.objects.get(id=user_id)
#             self.usernames.append(user.username)
#         self.unique_usernames.update(self.usernames)
#         return self.oshindonga

#     def definition_history(self):
#         self.definition = WordDefinition.history.all()
#         self.user_ids = []
#         for queryset in self.definition:
#             if queryset.history_user_id != None:
#                 self.user_ids.append(queryset.history_user_id)
#         for user_id in self.user_ids:
#             user = User.objects.get(id=user_id)
#             self.usernames.append(user.username)
#         self.unique_usernames.update(self.usernames)
#         return self.definition

#     def example_history(self):
#         self.example = DefinitionExample.history.all()
#         self.user_ids = []
#         for queryset in self.example:
#             if queryset.history_user_id != None:
#                 self.user_ids.append(queryset.history_user_id)
#         for user_id in self.user_ids:
#             user = User.objects.get(id=user_id)
#             self.usernames.append(user.username)
#         self.unique_usernames.update(self.usernames)
#         return self.example

#     def idiom_history(self):
#         self.idiom = OshindongaIdiom.history.all()
#         self.user_ids = []
#         for queryset in self.idiom:
#             if queryset.history_user_id != None:
#                 self.user_ids.append(queryset.history_user_id)
#         for user_id in self.user_ids:
#             user = User.objects.get(id=user_id)
#             self.usernames.append(user.username)
#         self.unique_usernames.update(self.usernames)
#         return self.idiom

#     def get_contributors(self, num=None):
#         self.reset_history()
#         self.english_history()
#         self.oshindonga_history()
#         self.definition_history()
#         self.example_history()
#         self.idiom_history()
#         contributors = []
#         for username in self.unique_usernames:
#             contributors.append((self.usernames.count(username), username))

#         def getKey(item):
#             return item[0]
#         contributors.sort(key=getKey, reverse=True)
#         top_contributors = contributors[:num]
#         return top_contributors


# <h3>Search for a word</h3>
#   <form action="" method="get">
#     <div class="row">
#       <div class="col-2 gx-0" id="input-language">
#         {{ form.input_language }}
#       </div>
#       <div class="col-6 gx-0">
#     <div class="input-group mb-3">

#       {{ form.search_word }}
#       <input class="btn btn-outline-primary" type="submit" value="Search" id="button-addon2"></input>
#     </div>
#       </div>
#       <div class="col-4"></div>
#     </div>
#   </form>
#   <ul id='suggested-searches'>
#     <li id='s-search-heading'><h6>Suggested searches:</h6></li>
#     <li class='s-searches'><a href='#'>home</a></li>
#     <li class='s-searches'><a href='#'>science</a></li>
#     <li class='s-searches'><a href='#'>tradition</a></li>
#     <li class='s-searches'><a href='#'>love</a></li>
#   </ul>
#   <br>
#   <h4>Search Results:</h4>
#   <div class="row">
#     <div class="col-8 columns">
#       {% if searched_word %}
#         <ol class="search-results-list">
#         {% for item in searched_word %}
#             <li>{{ item }}</li>
#         {% endfor %}
#       </ol>
#       <h5 class='definition'>Definitions</h5>
#         {% else %}
#           <p>No search was performed</p>
#         {% endif %}
#       {% for definition_object in definitions %}
#         <hr>
#         <h6 class='definition-object'>{{ definition_object }}</h6>
#         <hr>
#         {% if definition_object != 'No definition found' %}
#         <div class='div-english-definitions'><p><i class='definitions-heading'>English definitions</i></p>
#           <p>>{{ definition_object.english_definition }}</p></div>
#         <div class="examples-div">
#           <p><i class='examples-heading'>Examples:</i></p>
#           <ol class='examples-list'>
#             {% for example_object in examples %}
#               {% if example_object.definition_id == definition_object.id %}
#                 <li><i>{{ example_object.english_example }}</i></li>
#               {% elif example_object == 'No example found' %}
#                 <li><i>{{ example_object }}</i></li>
#               {% endif %}
#             {% endfor %}
#           </ol>
#         </div>
#         <div class="div-oshindonga-examples"><p><i class='definitions-heading'>Efatululo mOshindonga</i></p>
#           <p>>{{ definition_object.oshindonga_definition }}</p></div>
#           <div class="examples-div">
#             <p><i class='examples-heading'>Iiholelwa:</i></p>
#             <ol class='examples-list'>
#               {% for example_object in examples %}
#                 {% if example_object.definition_id == definition_object.id %}
#                   <li><i>{{ example_object.oshindonga_example }}</i></li>
#                 {% elif example_object == 'No example found' %}
#                   <li><i>Inapu monika oshiholelwa</i></li>
#                 {% endif %}
#               {% endfor %}
#             </ol>
#           </div>
#         {% endif %}
#       {% endfor%}
#     </div>
#     <div class="col-4 columns">
#       <h5><strong>Top Contributors: </strong></h5>
#       <ol>
#         <li>Contributor 1</li>
#         <li>Contributor 2</li>
#         <li>Contributor 3</li>
#         <li>Contributor 4</li>
#         <li>Contributor 5</li>
#         <li>Contributor 6</li>
#         <li>Contributor 7</li>
#         <li>Contributor 8</li>
#         <li>Contributor 9</li>
#         <li>Contributor 10</li>
#       </ol>
#     </div>
#   </div>

# "beautify.language": {


#         "js": {
#             "type": [
#                 "javascript",
#                 "json",
#                 "jsonc"
#             ],
#             "filename": [
#                 ".jshintrc",
#                 ".jsbeautifyrc"
#             ]
#         },
#         "css": [
#             "css",
#             "less",
#             "scss"
#         ],
#         "html": [
#             "htm",
#             "html"
#         ]
#     },
#     "beautify.ignore": "",
#     "beautify.config": ""
# }
# from datetime import datetime

# def add_new():
#     print("STARTED:", datetime.now())
#     count = 0
#     with open("english.txt", 'r', encoding='utf-8') as f:
#         for line in f:
#             try:
#                 word = line.strip()
#                 new_word = EnglishWord(word=word)
#                 new_word.save()
#                 count += 1
#             except:
#                 print(sys.exc_info()[0], "occurred.")
#     print(count, "New words were added)")
#     print("ENDED:", datetime.now())
#     return

# class MyLinkedList():
#     def __init__(self, value):
#         self.head = {'value': value, 'next': None}
#         self.tail = self.head
#         self.length = 1
#         self.nodes = [self.head, self.tail]

#     def __str__(self):
#         return str(self.head['value']) + "--->" + str(self.head['next'['value']])

#     def append(self, value):
#         current_node = {'value': value, 'next': None}
#         if self.length == 1:
#             self.head['next'] = current_node
#             self.tail = current_node
#             self.length += 1
#         else:
#             self.tail['next'] = current_node
#             self.tail = current_node
#             self.length += 1
#         return self

# l1 = MyLinkedList(10)
# print(l1.apend(5))
# from dictionary.models import WordDefinition
# definition_queryset = WordDefinition.objects.all()
# queryset_dict = {q[i].id:(q[i].english_definition, q[i].oshindonga_definition) for i in range(len(q))}
# print(q)
# print(len(q))
# print(q_dict)
from django.core.mail import send_mail
from django.conf import settings

subject = 'Welcome to the community'
message = f'Hi, Bibz, \nThank you for registering as a contributor. \nWe cannot wait to see your contribution.'
email_from = settings.EMAIL_HOST_USER
recipient_list = ['admin@festusabiatar.com', 'abiatarfestus@outlook.com']
send_mail(subject, message, email_from, recipient_list)


#eQueue#

# def queues(request, pk, join_message=None):
#     '''
#     If request method is GET, generate a view for the current queue of the service enrolment of the passed in pk.
#     If request method is POST, add the current user to the queue of the passed in service enrolment, if not already in queue.
#     '''
#     context = {}
#     # Return a queryset of customers queued up for the passed in service_enrolment
#     current_service_enrolment = ServiceEnrolment.objects.get(id=pk)
#     current_queue = QueuedCustomer.objects.filter(
#         service_enrolment_id=pk).order_by('join_time')  # A queryset of queuedCustomer instances filtered by the service_id
#     queue_length = len(current_queue) > 0
#     queued_users = []
#     if queue_length:
#         # A list of user objects in current_queue
#         queued_users = [customer.customer for customer in current_queue]
#     context['queued_users'] = queued_users    
#     context['there_is_queue'] = queue_length
#     context['current_queue'] = current_queue
#     context['service'] = current_service_enrolment.service
#     context['service_enrolment'] = current_service_enrolment
#     context['service_provider'] = current_service_enrolment.service_provider
#     context['requirements'] = current_service_enrolment.service_requirements
#     if request.method == "POST":
#         if request.user in queued_users:
#             join_message = 'Duplicate'
#         else:
#             QueuedCustomer.objects.create(
#                 customer=request.user, service_enrolment=current_service_enrolment)
#             join_message = "Success"
#     context['join_message'] = join_message
#     return render(request, 'equeue/queues.html', context)


# def exit_queue(request, pk):
#     '''
#     Retrieve an instance of QueuedCustomer where customer_id=current_user.id and service_id=pk and save it to a variable current_instance
#     Insert in the CancelledCustomer table a new entry with queue_id and customer_id of the current_instance instance
#     Delete the current_instance instance from the QueuedCustomer
#     Return to and refresh the queue page.
#     '''

#     current_instance = QueuedCustomer.objects.filter(
#         service_enrolment_id=pk, customer_id=request.user.id).get()
#     CancelledCustomer.objects.create(
#         queue_id=current_instance.id, customer_id=current_instance.customer.id, cancelled_by=request.user)
#     current_instance.delete()
#     return redirect('equeue:queues', pk=pk)


# def my_queues(request, pk):
#     context = {}
#     # A list to hold ids of the service_enrolments the current user/servant is assigned to
#     service_enrolment_ids = []
#     servant_enrolments = ServantEnrolment.objects.filter(servant_id=pk)
#     # print(f'PK: {pk}')
#     context['servant_enrolments'] = servant_enrolments
#     for entry in servant_enrolments:  # Loops through the servant_enrolments, extract the service_enrolment ids and add them to the list
#         service_enrolment_ids.append(entry.service_enrolment_id)
#         # print(f'SERVICE_ENROLMENT_IDs: {service_enrolment_ids}')
#     # QueuedCustomer instances with service_enrolment assigned to the current servant
#     eligible_queue = QueuedCustomer.objects.filter(
#         service_enrolment_id__in=service_enrolment_ids)
#     # eligible_queue_ids = []
#     # for entry in eligible_queue:
#     #     eligible_queue_ids.append(entry.service_enrolment_id)
#     #     print(f'ELIGIBLE_QUEUE_IDs: {eligible_queue_ids}')

#     eligible_queue_ids = {}
#     for entry in eligible_queue:
#         if entry.service_enrolment_id in eligible_queue_ids:
#             eligible_queue_ids[entry.service_enrolment_id] += 1
#         else:
#             eligible_queue_ids[entry.service_enrolment_id] = 1
#         # print(f'ELIGIBLE_QUEUE_IDs: {eligible_queue_ids}')
#     context['eligible_queue_ids'] = eligible_queue_ids
#     return render(request, 'equeue/my_queues.html', context)


# def serve_customers(request, pk, current_customer=0):
#     '''
#     Build the current_queue from QueuedCustomer using the service-enrolment id passed in as pk.
#     If called as a redirect from nex_customer, use the current_customer value to get served_customer from ServedCustmer.
#     Use served_customer.customer_id to determine the current_customer object from User.
#     The last_served_id holds the current_customer value, to be passed to the template and used as an argument to the next call of next_customer.

#     '''
#     # print(f'LAST_SERVED ID AS C_C: {current_customer}')
#     context = {'next_customer_message': None,
#                'current_customer': current_customer, 'last_served_id':current_customer}
#     if current_customer > 0:
#         served_customer = ServedCustomer.objects.get(id=current_customer)
#         context['current_customer'] = User.objects.get(id=served_customer.customer_id)
#     current_service_enrolment = ServiceEnrolment.objects.get(id=pk)
#     current_queue = QueuedCustomer.objects.filter(
#         service_enrolment_id=pk).order_by('join_time')  # A queryset of queuedCustomer instances filtered by the service_id
#     queue_length = len(current_queue) > 0
#     queued_users = []
#     if queue_length:
#         # A list of user objects in current_queue
#         queued_users = [customer.customer for customer in current_queue]
#     context['queued_users'] = queued_users
#     context['there_is_queue'] = queue_length
#     context['current_queue'] = current_queue
#     context['service'] = current_service_enrolment.service
#     context['service_enrolment'] = current_service_enrolment
#     context['service_provider'] = current_service_enrolment.service_provider
#     return render(request, 'equeue/serve_customers.html', context)


# def next_customer(request, pk, last_served_id):
#     '''
#     Retrieve an instance of QueuedCunstomer with an id denoted by the pk parameter passed to the request.
#     Save it in a variable front_customer (this is not a user, but a QueuedCustomer instance) and save it to the ServedCustomer table as a new entry with customer_id of the front_customer.
#     The new entry to ServedCustomer should have an initial service_duration = 0 (default), to be updated when the customer is done with.
#     Delete this record from the QueuedCustomer table (but not the instance itself since it should be passed to the re-direct function).
#     Redirect to the serve-customer view, passing in the id of front_customer's ServedCustomer instance as current_customer.
#     NB: current_customer in this function is the instance of ServedCustomr that has just been created, and its id is being passed to serve_customers.
#     '''
#     if last_served_id > 0: #When this is NOT the first custmer served
#         last_served = ServedCustomer.objects.get(id=last_served_id)
#         # print(f'LAST_SERVED: {last_served}')
#         duration = timezone.now()-last_served.date_time_served
#         seconds = int(duration.total_seconds())
#         # print(f'DURATION: {duration}')
#         # print(f'SECONDS: {seconds}')
#         last_served.service_duration = seconds
#         last_served.save()
#     front_customer = QueuedCustomer.objects.get(id=pk)
#     front_customer_id = front_customer.customer_id
#     ServedCustomer.objects.create(customer_id=front_customer_id,
#                                   service_enrolment_id=front_customer.service_enrolment_id, served_by=request.user)
#     current_customer = ServedCustomer.objects.filter(
#         customer_id=front_customer_id, service_enrolment_id=front_customer.service_enrolment_id, served_by=request.user).order_by('-date_time_served')
#     # print(f'CURRENT_CUSTOMER_IN_NEXT: {current_customer}')
#     served_id = current_customer[0].id
#     # print(f'SERVED_ID: {served_id}')
#     QueuedCustomer.objects.filter(id=pk).delete()
#     return redirect('equeue:serve-customers', pk=front_customer.service_enrolment_id, current_customer=served_id)


# def cancel_customer(request, pk):
#     return redirect('equeue:serve-customers', pk=pk)