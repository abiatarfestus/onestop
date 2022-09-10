from dictionary.models import WordDefinition


def update_pos():
    print("Running update query...")
    WordDefinition.objects.filter(part_of_speech="NOUN").update(part_of_speech="NN")
    WordDefinition.objects.filter(part_of_speech="ADJ").update(part_of_speech="JJ")
    WordDefinition.objects.filter(part_of_speech="ADP").update(part_of_speech="IN")
    WordDefinition.objects.filter(part_of_speech="ADV").update(part_of_speech="RB")
    WordDefinition.objects.filter(part_of_speech="AUX").update(part_of_speech="MD")
    WordDefinition.objects.filter(part_of_speech="CCONJ").update(part_of_speech="CC")
    WordDefinition.objects.filter(part_of_speech="DET").update(part_of_speech="DT")
    WordDefinition.objects.filter(part_of_speech="INTJ").update(part_of_speech="UH")
    WordDefinition.objects.filter(part_of_speech="NUM").update(part_of_speech="CD")
    WordDefinition.objects.filter(part_of_speech="PART").update(part_of_speech="RP")
    WordDefinition.objects.filter(part_of_speech="PRON").update(part_of_speech="PRP")
    WordDefinition.objects.filter(part_of_speech="PROPN").update(part_of_speech="NNP")
    WordDefinition.objects.filter(part_of_speech="SCONJ").update(part_of_speech="IN")
    WordDefinition.objects.filter(part_of_speech="VERB").update(part_of_speech="VB")
    print("Update finished!")
