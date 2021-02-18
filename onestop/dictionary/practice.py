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