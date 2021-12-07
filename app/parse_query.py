from word_forms.word_forms import get_word_forms

def parse_sentence(inputString):
    words = inputString.split()
    action_list = {}
    object_list = {}

    #Read all the action words and store it
    with open('hico_list_vb.txt') as f:
        lines = f.readlines()
    for i in range(2,len(lines)):
        row = lines[i].split()
        w = row[1].split("_")
        if len(w) == 2:
            temp = list(get_word_forms(w[0])['v'])
            action_list[row[1]] = [x+" "+w[1] for x in temp]
        else:
            action_list[row[1]] = list(get_word_forms(row[1])['v'])

    #Read all the objects and store it
    with open('hico_list_obj.txt') as f:
        lines = f.readlines()
    for i in range(2,len(lines)):
        row = lines[i].split()
        object_list[row[1]] = 1

    #Find action and object
    actions = []
    objects = []
    for w in words:
        if w in object_list:
            objects.append(w)
    
    for key,val in action_list.items():
        for form in val:
            if form in inputString:
                actions.append(key)

    return actions,objects

# ac,ob = parse_sentence("person riding a horse")
# print(ac,ob)