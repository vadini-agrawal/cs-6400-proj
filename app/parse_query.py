def parse_sentence(inputString):
    words = inputString.split()
    action_list = {}
    object_list = {}

    #Read all the action words and store it
    with open('../data/hico_20160224_det/hico_list_vb.txt') as f:
        lines = f.readlines()
    for i in range(2,len(lines)):
        row = lines[i].split()
        action_list[row[1]] = 1

    #Read all the objects and store it
    with open('../data/hico_20160224_det/hico_list_obj.txt') as f:
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
        if w[-3:] == "ing":
            ac = w[: len(w)-3]
            if ac in action_list:
                actions.append(ac)

    return actions,objects
