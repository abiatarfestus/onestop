def search_examples(definitions_pks):
    '''
        Takes in a list of pks of found definitions and search if examples exist and return example objects.
    '''
    examples = []
    for definition_pk in definitions_pks:
        try:
            example = DefinitionExample.objects.get(definition_id=definition_pk)  # Return a definition example object
            examples.append(example)
        except DefinitionExample.DoesNotExist:
            # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
            examples.append('No example found')
    context['examples'] = examples
    return render(request, 'dictionary/search.html', context)

def search_definitions(word_pairs_pks):
    '''
        Takes in a list pks of word pairs and return a list of pks of all definitions found.
    '''
    definitions = []
    for pair_pk in word_pairs_pks:
        try:
            definition = WordDefinition.objects.get(word_pair_id=pair_pk)  # Return a definitions of a word pair
            definitions.append(definition)
        except WordDefinition.DoesNotExist:
            # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
            definitions.append('No definition found')
    context['definitions'] = definitions
    definitions_pks = [
        definition.id for definition in definitions]
    #return definitions_pks
    search_examples(definitions_pks)

def search_word_pairs(eng_word_pk):
    '''
        Using the Enflish word pk (foreignkey id) search if for English|Oshindonga pairs and return a list of pks of all pair objects found.
    '''
    word_pairs = OshindongaWord.objects.filter(english_word_id=eng_word_pk)  # Return a queryset of all word pairs with the searched word
    if word_pairs == []:
        context['searched_word'] = 'The word you searched is not yet translated into Oshindonga.'
        return render(request, 'dictionary/search.html', context)
    else:
        context['searched_word'] = word_pairs
        # Etract pk/id of each pair and save them in a list
        word_pairs_pks = [
            word_pair.id for word_pair in word_pairs]
        #return word_pairs_pks
        search_word_pairs(word_pairs_pks)