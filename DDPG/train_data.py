import numpy as np
import collections
def split_features(item):
    # item = item.strip('\n')
    # print('item=',item)
    # item = item.split('\t')
    li=list()
    for i in range (4,11):
        li.append(float(item[i]))
        # print(i)
    # print(li)
    return li
def coll_features(single_state,temp_list,item):
    type2_feature=split_features(item)
    # print('type2_feature',len(type2_feature))
    if (len(single_state) == 0):
        la = temp_list + temp_list + temp_list
        # state_set.append(la)
        # return la
    if (len(single_state) == 1):
        temp = temp_list + temp_list

        ar = np.array(single_state[0])
        la = ar.tolist()
        # print('la=', la)
        la = temp + la
        # state_set.append(la)
        # return la
    if (len(single_state) == 2):
        temp = temp_list

        ar1 = np.array(single_state[0])
        la1 = ar1.tolist()
        # print('la=', la1)
        la = temp + la1
        ar2 = np.array(single_state[1])
        la2 = ar2.tolist()
        # print('la=', la2)
        la = la + la2
        # state_set.append(la)
        # return la
    if (len(single_state) == 3):
        la = np.array(single_state[0]).tolist() + np.array(single_state[1]).tolist() + np.array(
            single_state[2]).tolist()
        # state_set.append(la)
    next_state=la[7:]+type2_feature
        # print('coll_features',next_state)

    state=la+next_state
        # print('coll_features', state)
    return state
def split_skn(item):
    # show skn_id,skn
    show_skn=item[11]
    #click  skn
    click_skn=item[12]
    old_rank_sknid_list=item[13]
    return [show_skn,click_skn,old_rank_sknid_list]

def creat_state(path):
    # path='C:/Users/qingqing.sun/Downloads/'
    f = open(path, 'r')
    item=f.readline()
    temp_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    temp_state=collections.deque()
    last_uid=''
    dictionary = {}
    dic_set=collections.deque()
    state_set=collections.deque()
    skn_list_set=list()
    le=0
    uid_time=list()
    while item:
        # print(item)
        le+=1
        item = item.strip('\n')
        # print('item=',item)
        item = item.split('\t')
        # print(item)
        file_type=item[0]
        uid=item[2]
        time=item[3]


        if uid==last_uid or last_uid=='':
            # print('uid is same')
            # print('deque len=',len(temp_state))
            if(file_type=='1'):
                # print('type 1')
                if(len(temp_state)<3):
                    feature=split_features(item)
                    temp_state.append(feature)
                elif(len(temp_state)==3):
                    temp_state.popleft()

                    feature = split_features(item)
                    temp_state.append(feature)
                # print('temp_state=',temp_state)
            elif(file_type=='2'):
                # print('type 2')

                single_state=temp_state

                # single_state.clear()
                # single_state.append(temp_state)
                # single_state.append(item)
                # print('single_state=',single_state)
                la=coll_features(single_state,temp_list,item)
                # print('type =la',la)
                state_set.append(la)

                skn_list=split_skn(item)
                # print('skn_list=',skn_list)
                skn_list_set.append(skn_list)
                uid_time.append([uid, time])



        elif(uid!=last_uid):
            # print('uid is not same')
            temp_state.clear()
            if (file_type == '1'):

                feature = split_features(item)
                temp_state.append(feature)
                # print('type 1temp_state=', temp_state)
            elif(file_type=='2'):

                single_state = temp_state
                # single_state.clear()
                # single_state.append(temp_state)
                # single_state.append(item)

                # ar = np.array(single_state)
                # la = ar.tolist()
                # state_set.append(la)

                # print('type 2 single_state=', single_state)

                la = coll_features(single_state, temp_list,item)
                # print('type != la', la)
                state_set.append(la)
                skn_list = split_skn(item)
                # print('skn_list=', skn_list)
                skn_list_set.append(skn_list)
                uid_time.append([uid, time])

        last_uid=uid



        item=f.readline()
    # print('state_set',state_set)
    states = np.array(state_set)
    # print(states[1])
    # print('dic_set', dic_set)
    st_len=len(state_set)
    state_len = len(states)
    skn_set=np.array(skn_list_set)
    skn_len=len(skn_set)
    print(st_len)
    print(state_len)
    print(skn_len)
    # print(np.array(skn_list_set)[1][0])
    # print('creat',states[0])
    # print(state_set[2])

    return states,skn_set
def get_skn_feature_map(path):
    # path = 'C:/Users/qingqing.sun/Downloads/'
    f = open(path , 'r')
    item = f.readline()
    skn_feature=dict()
    le=0
    while item:
        le+=1
        item = item.strip('\n')
        # print('item=',item)
        item = item.split('\t')
        # print(item)
        feature=list()
        for i in range(3,10):
            feature.append(item[i])

        skn_feature[item[0]]=feature

        item = f.readline()
    # skn_feature.
    print(len(skn_feature))
    # print(skn_feature['51782474'])
    return skn_feature
def get_label(show_skn,click_skn):
    # print('type', len(click_skn))
    # print(click_skn)
    click_skn_len=0
    if click_skn == '[]':
        # print('is  null')
        click_skn_len=0
    else:
        click_skn = click_skn.strip('[')
        click_skn = click_skn.strip(']')
        click_skn = click_skn.split(',')

        # print(click_skn)
        # print('click', len(click_skn))
        click_skn_len=len(click_skn)
    # print('show_skn', show_skn)
    single_query_feature = list()
    # for i in range(len(show_skn)):
    i = len(show_skn) - 1
    show_skn = show_skn.strip('[')
    show_skn = show_skn.strip(']')
    show_skn = show_skn.split(',')
    # print(show_skn)

    # print('show', len(show_skn))

    label = np.zeros(len(show_skn))
    # print(' bef label', label)
    j = 0
    for i in range(len(show_skn)):

        # print('i', i)
        # print('j', j)
        # print(show_skn[i])
        if (j >= click_skn_len):
            break
        # print(click_skn[j])
        if (show_skn[i] == click_skn[j]):
            # print('equel')
            label[i] = 1
            i += 1
            j += 1
        else:
            label[i] = 0
            i += 1

    # print('label', label)
    return label,show_skn,click_skn_len
def cal_potential_function(new_label,action,features_arr):

    return 0
def cal_reward(new_label,old_label,action,features_arr):
    predic_score = list()
    for i in range(len(features_arr)):
        feat = features_arr[i]
        score = 0.0
        for i in range(7):
            # print(float(feat[0]))
            score += action[i] * float(feat[i])

        predic_score.append(score)

    # print(type(np.cast(feat[0], float)))

    print('predic_score', predic_score)
    predict_score = np.array(predic_score)
    new_label = np.array(new_label)
    # print('predic_score', (predic_score))
    # print('new_label', (new_label))
    new = np.dstack((predict_score, new_label))
    # print('new', new[0].shape)
    reinf = new[0].tolist()
    print('recinf_new', reinf)
    # ############################
    potential_function_value=0
    x_w=0
    log_exp_x_w=0
    # import math
    for k in range(len(reinf)):
        potential_function_value+=reinf[k][0]*reinf[k][1]-np.log(1+np.exp(reinf[k][0]))

        x_w+=reinf[k][0]*reinf[k][1]
        log_exp_x_w+=np.log(1+np.exp(reinf[k][0]))
    ######################
    # ne.sort(reverse=True)
    # print('ne', reinf)
    reinf.sort(reverse=True)
    print('reinf  sort', reinf)

    #######################################
    sort_potential_function_value = 0

    # import math
    for k in range(len(reinf)):
        sort_potential_function_value += reinf[k][0] * reinf[k][1] - np.log(1 + np.exp(reinf[k][0]))
    ##########################################



    labe = new_label.tolist()
    labe.sort(reverse=True)
    # print('labe', labe)
    idcg = 0
    new_dcg = 0

    for j in range(len(labe)):
        # for j in range(20):
        # print(ideal_sorts[j])
        # print(numpy.log2(2+j))
        pre = reinf[j]
        # print(pre)
        new_dcg += ((2 ** pre[1]) - 1) / np.log2(2 + j+1)
        # print('new_dcg=',new_dcg)
        idcg += ((2 ** labe[j]) - 1) / np.log2(2 + j+1)
        # print('idcg=',idcg)


        # print(pre)
    # print('x_w',x_w)
    # print('log_exp_x_w', log_exp_x_w)
    # print('potential_function_value',potential_function_value)
    # print('sort_potential_function_value', sort_potential_function_value)
    # print('new_dcg_sum', new_dcg)
    new_dcg = new_dcg / len(reinf)

    idcg = idcg / len(labe)
    # print('new_dcg', new_dcg)
    # print(idcg)
    new_ndcg = new_dcg / idcg
    # print('new_ndcg', new_ndcg)
    old_dcg=0
    old_idcg=0
    old_labe=old_label.tolist()
    old_labe.sort(reverse=True)
    for j in range(len(old_label)):
        old_dcg += ((2 ** old_label[j]) - 1) / np.log2(2 + j + 1)
        old_idcg+=((2 ** old_labe[j]) - 1) / np.log2(2 + j+1)
    old_dcg/=len(old_label)
    old_idcg/=len(old_label)
    old_ndcg=old_dcg/old_idcg
    return new_ndcg,old_ndcg,potential_function_value

def get_new_old_label(show_skn,click_skn,old_rank_skn):
    # print('type', len(click_skn))
    # print(click_skn)
    click_skn_len=0
    if click_skn == '[]':
        # print('is  null')
        click_skn_len=0
    else:
        click_skn = click_skn.strip('[')
        click_skn = click_skn.strip(']')
        click_skn = click_skn.split(',')

        # print(click_skn)
        # print('click', len(click_skn))
        click_skn_len=len(click_skn)
    # print('show_skn', show_skn)
    single_query_feature = list()
    # for i in range(len(show_skn)):
    # i = len(show_skn) - 1
    # show_skn = show_skn.strip('[')
    # show_skn = show_skn.strip(']')
    # show_skn = show_skn.split(',')
    # print(show_skn)

    # print('show', len(show_skn))
    new_label=label(show_skn,click_skn)
    old_label=label(old_rank_skn,click_skn)

    return new_label,old_label,show_skn,click_skn_len
def label(show_skn,click_skn):

    click_skn_len = len(click_skn)
    new_label = np.zeros(len(show_skn))
    # print(' bef label', label)
    j = 0
    for i in range(len(show_skn)):

        # print('i', i)
        # print('j', j)
        # print(show_skn[i])
        if (j >= click_skn_len):
            break
        # print(click_skn[j])
        if (show_skn[i] == click_skn[j]):
            # print('equel')
            new_label[i] = 1
            i += 1
            j += 1
        else:
            new_label[i] = 0
            i += 1

    # print('label', new_label)
    return new_label

# if __name__ == '__main__':
#     path='C:/Users/qingqing.sun/Downloads/0/temp_pre_state_data_0115.txt'
#     state_set, skn_list=creat_state(path)
def skn_data_split(show_skn_id,click_skn,old_rank_id):
    # show_skn_id=skn_list[0][0]
    # click_skn=skn_list[0][1]
    # old_rank_id=skn_list[0][2]
    # print((show_skn_id))
    show_skn_id=show_skn_id.strip('[')
    show_skn_id = show_skn_id.strip(']')
    show_skn_id=show_skn_id.split('",')
    # show_skn_id = show_skn_id.split(',')
    # print(len(show_skn_id))
    skn_id_map=dict()
    show_skn=list()
    for i in range(len(show_skn_id)):
        skn_id = show_skn_id[i]
        # if(i<len(show_skn_id)-1):
        skn_id=skn_id.strip('"')
        skn_id=skn_id.split(',')
        skn_id_map[skn_id[0]]=skn_id[1]
        show_skn.append(skn_id[1])
        # else:
    # print(skn_id_map)
    # print(show_skn)




    # print((click_skn))
    # print(old_rank_id)
    old_rank_id=old_rank_id.split(',')
    old_rank_skn=list()
    for i in range(len(old_rank_id)):
        if old_rank_id[i] in skn_id_map.keys():
            old_rank_skn.append(skn_id_map[old_rank_id[i]])
    # print(old_rank_skn)
    return (show_skn, click_skn, old_rank_skn)




