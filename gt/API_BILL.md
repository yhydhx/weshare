#第一步，找到该用户

%%url: /user/show/{user_id}

function:
%%{user_id}即为host的id，可以为空
1. 显示查看host的具体信息
2. 显示该host下的留言

API:
正确的返回信息：
%%当用户登录的时候
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message: Char # 错误的提示信息
	data: {
		'user' : {
			"username" : char
			"gender" : int   ~ 1是男生0是女生
			"motto" : char   ~ 座右铭
			"introduction" : char  ~简介
			"icon" : char  ~ 头像
			"orders" : int  ~订单数量
			"service_time" : char ~提供服务的时间
			"max_payment" : float  
			"min_payment" : float 
				
			"state" : int  ~状态 normal user  => 0  examing => 1  sharer => 2
			"birth" : char ~生日
			"qq_number" : char ~qq号码
			"wechat" : char ~微信号

			%%Education Infomation
			"education" : int  ~目前的学历 bachlor => 0  graduate => 1 phd => 2 else => 3
			"bacholor" : char ~本科学校
			"graduate" : char  ~硕士学校
			"phd" : char  ~ 博士学校

			‘features’ : [
				'{topic_id}':{
					'name' : ~ char 话题的名字
	                'features' : [       ~所有feature的名字
	                	'{feature_name_1}':  ~特征1的名字
	                	'{feature_name_2}':  ~特征2的名字
	                	'{feature_name_3}':  ~特征3的名字
	                	......
	                ]
	                'row1' : [  ~第一列的特征的名字
	                	'{feature_name_1}':  ~特征1的名字
	                	'{feature_name_2}':  ~特征2的名字
	                	'{feature_name_3}':  ~特征3的名字
	                	......
	                ],
	                'row2' : [	~第二列的特征的名字
	                	'{feature_name_1}':  ~特征1的名字
	                	'{feature_name_2}':  ~特征2的名字
	                	'{feature_name_3}':  ~特征3的名字
	                	......
	                ],
	                'row3' : [ 	~第三列的特征的名字
	                	'{feature_name_1}':  ~特征1的名字
	                	'{feature_name_2}':  ~特征2的名字
	                	'{feature_name_3}':  ~特征3的名字
	                	......
	                ],
	                'row4' : [	~第四列的特征的名字
	                	'{feature_name_1}':  ~特征1的名字
	                	'{feature_name_2}':  ~特征2的名字
	                	'{feature_name_3}':  ~特征3的名字
	                	......
	                ],
				},
			]
		}，

		'questions':[
			{
				'feature_name'  :   ~  问题的名字 
            	'feature_id'  :   ~ 	问题的id
            	'm_id'  	:    ~		问题的小话题
            	't_id'		:  ~  		问题的大话题
			},{
				'feature_name'  :   ~  问题的名字 
            	'feature_id'  :   ~ 	问题的id
            	'm_id'  	:    ~		问题的小话题
            	't_id'		:  ~  		问题的大话题
			},
			....
		]
		'msgs' : ""   ~提示信息
		'current_user' : {   ~当前登录的用户的信息
			"username" : char
			"gender" : int   ~ 1是男生0是女生
			"motto" : char   ~ 座右铭
			"introduction" : char  ~简介
			"icon" : char  ~ 头像
			"orders" : int  ~订单数量
			"service_time" : char ~提供服务的时间
			"max_payment" : float  
			"min_payment" : float 
				
			"state" : int  ~状态 normal user  => 0  examing => 1  sharer => 2
			"birth" : char ~生日
			"qq_number" : char ~qq号码
			"wechat" : char ~微信号

			%%Education Infomation
			"education" : int  ~目前的学历 bachlor => 0  graduate => 1 phd => 2 else => 3
			"bacholor" : char ~本科学校
			"graduate" : char  ~硕士学校
			"phd" : char  ~ 博士学校
		}
		'login_flag' : 1





第二步，提交订单初始化信息
%%url: /bill/init

method : POST

function:

1. 提交feature的名字和host的id
2. 初始化预约信息

API:

提交信息

{
	'feature_id'
	'host_id'
	'intro_and_question'         ~介绍情况和问题
    'appointment_time'       ~约定的时间和时间长度	
}


正确的返回信息：
%%当用户登录的时候
跳转走了


第三步： 管理订单：
%%url: /host_center/manage

method : GET

function:

1. 查看当前用户的所有订单，如果用户是guest的话，只有一类订单，如果用户是host的话，那么可能会有两类订单
2. 初始化预约信息

API:

返回信息

%%如果用户是host的话，会有  字段 ’got_bills‘，如果用户只是一个guest的话， 只有字段 ’sent_bills‘

%%只显示相关的数据

data = {
	’got_bills‘:[
		{
			
	        'host_name'  :     ~  分享着的名字
	        'host_motto'  :     ~  分享者的一句话简介
	        'state'  :     ~  目前的订单状态    0,    #创建订单  1,    #等待确认   2,   #等待付款   3,   #完成了付款   4     #结算完成
	        'from_user_id'  :     ~  
	        'to_host_id'  :     ~  
	        'from_user_icon'  :     ~  
	        'to_host_icon'  :     ~  
	        'intro_and_question'  :     ~  
	        'appointment_time'  :     ~  
	        'recommend_info'  :     ~  
	        'recommend_begin_time'  :     ~  
	        'recommend_end_time'  :     ~  
	        'recommend_length'  :     ~  
	        'feature_name'     :     	~ 话题内容
	        'appointment_init_time':    ~订单创建时间
 	        'appointment_id'  :     ~  唯一的订单号
		}
	]
}


第四步，查看订单，用户通过唯一的订单号进入，后端判断是进入的是需求方还是被需求方
%%url: /bill/detail/{订单的ID}

method : GET

function:

1. 检测订单的请求者是不是目前登录的用户
2. 传输相应的订单数据

API:
%%如果这个人是这个订单的guest
template :  'frontEnd/appoint_guest.html'
 
data = {
	'appointment'  : {
						'id':         ~该订单的唯一标示符号
				        'state'  :     ~  目前的订单状态    0,    #创建订单  1,    #等待确认   2,   #等待付款   3,   #完成了付款   4     #结算完成
				        'from_user_id'  :     ~  
				        'to_host_id'  :     ~  
				        'from_user_icon'  :     ~  
				        'to_host_icon'  :     ~  
				        'intro_and_question'  :     ~  
				        'appointment_time'  :     ~  
				        'recommend_info'  :     ~  
				        'recommend_begin_time'  :     ~  
				        'recommend_end_time'  :     ~  
				        'recommend_length'  :     ~  
				        'appointment_id'  :     ~  唯一的订单号
					}
	'messages':[
		{
			'from_user_name' 			~发文的用户名
            'user_icon' 			~用户icon
            'message' 			~信息
		},{
			'from_user_name' 			~发文的用户名
            'user_icon' 			~用户icon
            'message' 			~信息
		},{
			'from_user_name' 			~发文的用户名
            'user_icon' 			~用户icon
            'message' 			~信息
		}...
	]
}


%%如果这个是这个订单的host
template :  'frontEnd/appoint_host.html',Info)



第五步：
在 host 的 url: /bill/detail/{订单的ID}中
Guest确认订单，

url:   /bill/host_certify
method ： post
%%  注意：时间的格式用  "2015-1-1 12:00:00" 这种，否则无法存储
%%appnt_id 不是订单号, 而是订单这个类的ID

{
	    'recommend_info' :   			~建议的信息
        'recommend_begin_time' :   		~建议的开始时间
        'recommend_end_time' :   		~建议的结束时间
        'recommend_length' :   			~建议的时长
        'appnt_id' :   					~订单的ID
}




第六步：
双方交涉，谈好了一个大概的价钱和时间
相当于评论功能，哈哈哈哈哈哈

url : /bill/communicate
method : POST

{
	'appnt_id':    ~ 订单的ID
	'message': 			~ 用户输入的数据
}


第七步：
付款付款

url : /bill/pay
method : POST

{
	'appnt_id':    ~ 订单的ID
	'message': 			~ 用户输入的数据
}

