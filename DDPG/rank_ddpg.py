from ddpg import *
from space_set import makeEnv
TRAIN_NUM=163383
# TRAIN_NUM=1500
TEST=163383
EPISODES = 1
import train_data
path='C:/Users/qingqing.sun/Downloads/0/data/'
# temp_pre_state_data_0115.txt

def main():
    # env=makeEnv()
    agent = DDPG()
    state_set,skn_list=train_data.creat_state(path+'test_pre_state_data_0116.txt')
    TRAIN_NUM=len(state_set)
    # print(type(state_set))
    # print(state_set.shape)
    # train_raward=0
    skn_features_map = train_data.get_skn_feature_map(path+ 'skn_features_0115.txt')
    num_index=0
    for episode in range(EPISODES):
        train_raward = 0
        train_old_ndcg=0
        for state_num in range(TRAIN_NUM - 1):
        # for state_num in range(10):
            num_index+=1
            # print('num_index',num_index)
            # print('uid_time',uid_time[state_num])
    # for state_num in range(15):
            state=state_set[state_num][0:21]
            print(state_set[state_num])
            # print('feature_num',len(state_set[state_num]))
        # action = agent.noise_action(state)
            action = agent.action(state)
            print('action', action)

            show_skn_id=skn_list[state_num][0]

            click_skn = skn_list[state_num][1]

            old_rank_id=skn_list[state_num][2]

            show_skn, click_skn, old_rank_skn=train_data.skn_data_split(show_skn_id, click_skn, old_rank_id)
            # print('show_skn',show_skn)
            # print('click_skn', click_skn)
            # print('old_rank_skn', old_rank_skn)
            new_label, old_label, show_skn, click_skn_len=train_data.get_new_old_label(show_skn, click_skn, old_rank_skn)
            # print('new_label=',new_label)
            # print('old_label=', old_label)
            # label,show_skn,click_skn_len=train_data.get_label(show_skn_str, click_skn)
            if(click_skn_len==0):
                reward=0
            else:
        #
                features = list()
                for i in range(len(show_skn)):
                    skn_key = show_skn[i]
                    if (skn_key in skn_features_map.keys()):

                    # print('if')
                    # print(skn_features_map[skn_key])
                    # print(skn_features_map['51455052'])
                        feature = skn_features_map[skn_key]
                        features.append(feature)
                    else:
                        feature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                        features.append(feature)
                # print('features_len',len(features))
                features_arr = np.array(features)

                new_ndcg, old_ndcg,potential_function_value=train_data.cal_reward(new_label, old_label, action, features_arr)
                # print('new_ndcg', new_ndcg)
                # print('old_ndcg', old_ndcg)

                # reward=train_data.cal_reward(label, action, features_arr)
                reward=potential_function_value
            print('reward',new_ndcg)
            train_raward+=new_ndcg
            train_old_ndcg+=old_ndcg
            next_state=state_set[state_num][21:]
            # print('next_state_len',len(next_state))
            # agent.perceive(state, action, new_ndcg, next_state, False)
            agent.perceive(state, action, reward, next_state, False)
            # afteraction = agent.action(state)
            # print('after action',afteraction)
            # afternew_ndcg, afterold_ndcg, afterpotential_function_value = train_data.cal_reward(new_label, old_label, afteraction,
            #                                                                      features_arr)
            # print('afternew_ndcg', afternew_ndcg)
        ave_trainreward = train_raward / (TRAIN_NUM-1)
        ave_train_old_ndcg = train_old_ndcg / (TRAIN_NUM - 1)
    # agent.save_network(EPISODES)
    print('train Average Reward:', ave_trainreward)
    print('train Average old:', ave_train_old_ndcg)

    # agent.load_network()
    # # test
    # state_set_test, skn_list_test = train_data.creat_state(path + 'test_pre_state_data_0116.txt')
    # skn_features_map_test = train_data.get_skn_feature_map(path + 'skn_features_0116.txt')
    # #testing
    # total_reward = 0
    # test_old_ndcg=0
    # # for j in range(TEST-TRAIN_NUM,TEST):
    # excp=0
    # TEST=len(state_set_test)-1
    # for j in range(TEST):
    #     state=state_set_test[j][0:21]
    #     action = agent.action(state)
    #
    #     print('action', action)
    #     show_skn_id = skn_list_test[j][0]
    #
    #     click_skn = skn_list_test[j][1]
    #
    #     old_rank_id = skn_list_test[j][2]
    #
    #     show_skn, click_skn, old_rank_skn = train_data.skn_data_split(show_skn_id, click_skn, old_rank_id)
    #     new_label, old_label, show_skn, click_skn_len = train_data.get_new_old_label(show_skn, click_skn, old_rank_skn)
    #     # show_skn_str = skn_list_test[j][0]
    #
    #     # click_skn = skn_list_test[j][1]
    #     # label, show_skn, click_skn_len = train_data.get_label(show_skn_str, click_skn)
    #     if (click_skn_len == 0):
    #         excp+=1
    #         continue
    #         reward = 0
    #     else:
    #         #
    #         features = list()
    #         for i in range(len(show_skn)):
    #             skn_key = show_skn[i]
    #             if (skn_key in skn_features_map_test.keys()):
    #
    #                 # print('if')
    #                 # print(skn_features_map[skn_key])
    #                 # print(skn_features_map['51455052'])
    #                 feature = skn_features_map_test[skn_key]
    #                 features.append(feature)
    #             else:
    #                 feature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #                 features.append(feature)
    #                 # print(np.array(features))
    #         features_arr = np.array(features)
    #         new_ndcg, old_ndcg ,potential_function_value= train_data.cal_reward(new_label, old_label, action, features_arr)
    #         # reward = train_data.cal_reward(label, action, features_arr)
    #     print('reward', new_ndcg)
    #     print('old_ndcg', old_ndcg)
    #     total_reward += new_ndcg
    #     test_old_ndcg+=old_ndcg
    # ave_test_reward = total_reward / (TEST-excp)
    # test_ave_old_ndcg=test_old_ndcg/(TEST-excp)
    # print('TEST=',TEST)
    # print('excp=',excp)
    # print('train Average Reward:', ave_trainreward)
    # print('train Average old:', ave_train_old_ndcg)
    # print('Evaluation Average Reward:', ave_test_reward)
    # print('Evaluation old ndcg:', test_ave_old_ndcg)





################################


    # for episode in range(EPISODES):
    #     state = env.reset()
    #     #print "episode:",episode
    #     # Train
    #     for step in range(env.spec.timestep_limit):
    #         action = agent.noise_action(state)
    #         next_state,reward,done,_ = env.step(action)
    #         agent.perceive(state,action,reward,next_state,done)
    #         state = next_state
    #         if done:
    #             break
        # Testing:
    #     if episode % 100 == 0 and episode > 100:
		# 	total_reward = 0
		# 	for i in range(TEST):
		# 		state = env.reset()
		# 		for j in range(env.spec.timestep_limit):
		# 			#env.render()
		# 			action = agent.action(state) # direct action for test
		# 			state,reward,done,_ = env.step(action)
		# 			total_reward += reward
		# 			if done:
		# 				break
		# 	ave_reward = total_reward/TEST
		# 	print 'episode: ',episode,'Evaluation Average Reward:',ave_reward
    # env.monitor.close()

if __name__ == '__main__':
    main()
