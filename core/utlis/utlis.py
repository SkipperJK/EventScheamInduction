

def find_sub_obj(trigger, words):
    sub = None
    obj = None
    trigger_id = trigger['id']
    for i, word in enumerate(words):
        if i+1 == trigger_id:
            continue
        if word['head_id'] == trigger_id:
            if word['dependency'] == '主谓关系' and word['postag'][0] == 'n':
                sub = word
            elif word['dependency'] == '动宾关系' and word['postag'][0] == 'n':
                obj = word
    return sub, obj