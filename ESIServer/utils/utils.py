

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


def is_entity(word):
    """判断词单元是否实体
    Args:
        entry: WordUnit，词单元
    Returns:
        *: bool，实体(True)，非实体(False)
    """
    # 候选实体词性列表
    # 人名，机构名，地名，其他名词，缩略词
    entity_postags = {'nh', 'ni', 'ns', 'nz', 'j'}
    if word.postag in entity_postags:
        return True
    else:
        return False