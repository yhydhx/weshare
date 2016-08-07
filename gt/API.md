Index 

url: /

template: 'front/index.html'

function:

API:

Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message: Char # 错误的提示信息
	data: {
		'object': [
			{
				'name': char # 省份名字
				'id': int # 省份 ID
				'schools': [
					{
						'name':  char # 学校的名字
						'id': char # 学校的独立ID
					}，
					{
						'name':  char # 学校的名字
						'id': char # 学校的独立ID
					}，
					...
				]
			},
			{
				'name': char # 省份名字
				'id': int # 省份 ID
				'schools': [
					{
						'name':  char # 学校的名字
						'id': char # 学校的独立ID
					}，
					{
						'name':  char # 学校的名字
						'id': char # 学校的独立ID
					}，
					...
				]
			},
			...
		]，

		'topics': [
			{
				'name' : char # 话题姓名
	            'tag' : char # 话题标签
	            'number' : int # 话题中包含用户的数量
	            'index' : int # 话题的位置
	            'topics' : {    # 里面包含每个用户的ID
	            	host_id_1 : 1,
	            	host_id_2 : 2,
	            	...
	            } 	
			},{
				'name' : char # 话题姓名
	            'tag' : char # 话题标签
	            'number' : int # 话题中包含用户的数量
	            'index' : int # 话题的位置
	            'topics' : {    # 里面包含每个用户的ID
	            	host_id_1 : 1,
	            	host_id_2 : 2,
	            	...
	            } 	
			},
			...
		]

		'hosts' : [
			{
				"username" : char
			    gender : int   # 1是男生0是女生
			    motto : char   # 座右铭
			    introduction : char  #简介
			    icon : char  # 头像
			    orders = int  #订单数量
			    service_time = char #提供服务的时间
			    max_payment = float  
			    min_payment = float 
			    
			    state = int   #状态 normal user  => 0  examing => 1  sharer => 2

			    birth = char #生日
			    qq_number = char #qq号码
			    wechat = char #微信号

			    #Education Infomation
			    education = int  #目前的学历 bachlor => 0  graduate => 1 phd => 2 else => 3
			    bacholor = char #本科学校
			    graduate = char  #硕士学校
			    phd = char  # 博士学校
			},
			......
		],

		'register_num' : int #  注册人数
        'host_num' : int # 分享者人数
        'normal_num' : int # 普通用户人数
        'school_num' : int # 学校数量
	}
}



url: /complete_account_feature

method: post
提交的数据

	{
		"topic_id" :  char  # 话题的ID
		"feature_name" : char  # 新增的feature的名字
 		"topic_tag" : char  # 话题的tag，用来识别topic
	}


返回：

{
        'state' : = 0
        'message' : = ""
		'data' : = {
			'topic_tag' : char  #话题的tag，用来识别topic
        	'feature_name' : char  #新增的feature的名字
		}
       
}

method: get

无需提交数据