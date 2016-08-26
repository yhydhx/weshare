#用户
url: /api/user/register

method: post

function:
1. 用户注册信息
2. 检测部分字段是否为空
3. 检测密码
4. 返回错误信息



API:
前段提交数据


-----------------普通注册--------------
{
	'username' :   ~用户名
	'phone' :   ~手机号
	'email' :   ~邮箱
	'password:   ~密码
    'password_confirm  ~密码验证
	
}

-----------------通过API注册--------------
{
	'username' :   ~用户名
	'phone' :   ~手机号
	'email' :   ~邮箱
	'password:   ~密码
    'password_confirm  ~密码验证
	
	%%新的字段
	"icon":     ~用户的图片，如果没有设置为空
	"union_id"  ~ 腾讯提供的唯一标示符
}


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {}

%%错误的返回信息:

Info = {
	state: Int # 非零数字表示不成功
	message : ~ 错误提示信息
	data:{}
}

-----------------------------------------------------------------------------------------------
url: /api/user/login

method: post

function:
1. 用户登录
2. 返回提示信息

API:
%%用户提交
{
	'email' :  ~ 用户邮箱 
	'password' :  ~用户密码
}


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {}

%%错误的返回信息:

Info = {
	state: Int # 非零数字表示不成功
	message : ~ 错误提示信息
	data:{}
}


-----------------------------------------------------------------------------------------------
%%用户利用微信或者其他方式登录
url: /api/user/qqlogin

method: post

function:
1. 利用qq的接口登录，
2. 如果是第一次登录的话，返回信息并让其修改补充，如果是第二次登录的话，直接登录成功

API:
%%用户提交
{
	'username'    ：    ~用户的昵称
    'icon'    ：    		~用户的头像
    'union_id'    ：    ~腾讯提供的唯一的id
}


%%用户第一次登录的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {
		’registed' : False
		'username'    ：    ~用户的昵称
	    'icon'    ：    		~用户的头像
	    'union_id'    ：    ~腾讯提供的唯一的id
	}

----》 然后转到注册的那块


%%用户第一次登录的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {
		’registed' : True
	}

%%错误的返回信息:

Info = {
	state: Int # 非零数字表示不成功
	message : ~ 错误提示信息
	data:{}
}

-----------------------------------------------------------------------------------------------
url: /api/user/logout

method: get

function:
1. 用户登出
2. 返回提示信息

API:
%%用户无需提交


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'成功登出'  Char # 错误的提示信息
	data: {}

%%错误的返回信息:

Info = {
	state: Int # 非零数字表示不成功
	message : ~ 错误提示信息
	data:{}
}



-----------------------------------------------------------------------------------------------
url: /host_center/edit
template: frontEnd/center-edit.html
method: get

function:
1. 

API:


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {
		'host':{
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
			"education" : int  ~目前的学历 -1表示未填写 bachlor => 0  graduate => 1 phd => 2 else => 3
			"bacholor" : char ~本科学校
			"graduate" : char  ~硕士学校
			"phd" : char  ~ 博士学校
		}
	}

-----------------------------------------------------------------------------------------------
url: /host_center/manage
template: frontEnd/center-manage.html
method: get

function:
1. 

API:


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {
		'host':{
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
			"education" : int  ~目前的学历 -1表示未填写 bachlor => 0  graduate => 1 phd => 2 else => 3
			"bacholor" : char ~本科学校
			"graduate" : char  ~硕士学校
			"phd" : char  ~ 博士学校
		}
	}

-----------------------------------------------------------------------------------------------
url: /host_center/auth
template: frontEnd/center-auth.html
method: get

function:
1. 

API:


%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message:'注册成功，请登录'  Char # 错误的提示信息
	data: {
		'host':{
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
			"education" : int  ~目前的学历 -1表示未填写 bachlor => 0  graduate => 1 phd => 2 else => 3
			"bacholor" : char ~本科学校
			"graduate" : char  ~硕士学校
			"phd" : char  ~ 博士学校
		}
	}






-----------------------------------------------------------------------------------------------



#Index 

url: /api/index

function:
1. 显示话题信息及其包含的用户
2. 显示网站的统计数据
3. 显示部分用户（最多*人）
4. 用户是否在线
5. 显示前几个学校

API:
%%正确的返回信息：
Info = {
	state: Int # 0 表示成功，其他数字表示不成功
	message: Char # 错误的提示信息
	data: {
		"schools": [
			{
		        "s_province": 			# 学校所代表的省份
		        "s_image": 				#学校的图片
		        "s_name": 				~学校的姓名
		        "s_display_index": 		~暂时是无关变量
		        "s_student_number": 	~学校有学生的姓名
		    },
		    {
		        "s_province": 			# 学校所代表的省份
		        "s_image": 				#学校的图片
		        "s_name": 				~学校的姓名
		        "s_display_index": 		~暂时是无关变量
		        "s_student_number": 	~学校有学生的姓名
		    },
		    {
		        "s_province": 			# 学校所代表的省份
		        "s_image": 				#学校的图片
		        "s_name": 				~学校的姓名
		        "s_display_index": 		~暂时是无关变量
		        "s_student_number": 	~学校有学生的姓名
		    },
		    ......
		]
		'topics': [
			{
				'name' : char ~话题姓名
				'tag' : char ~ 话题标签
				'number' : int ~ 话题中包含用户的数量
				'index' : int ~ 话题的位置
				'topics' : {    ~ 里面包含每个用户的ID
					host_id_1 : 1,
					host_id_2 : 2,
					...
				} 	
			},{
				'name' : char ~ 话题姓名
				'tag' : char ~ 话题标签
				'number' : int ~ 话题中包含用户的数量
				'index' : int ~ 话题的位置
				'topics' : {    ~ 里面包含每个用户的ID
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
			},
			......
		],

		'register_num' : int ~ 注册人数
		'host_num' : int ~ 分享者人数
		'normal_num' : int ~ 普通用户人数
		'school_num' : int ~ 学校数量
		'login_flag' : int ~ 用户是否在线 0表示不在线，1表示在线
	}
}

错误的返回信息：
待定

-----------------------------------------------------------------------------------------------

#user 

%%url: /api/user/show/{user_id}

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

%%当用户未登录的时候
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
				}
			]
		}，

		'msgs' : ""   ~提示信息
		'current_user' : None ~用户未登录，显示信息为空
		'login_flag' = 0

错误的返回信息：

Info = {
	state: 404   Int # 0 表示成功，其他数字表示不成功
	message: ‘找不到该用户’   Char # 错误的提示信息
	data: {}


-----------------------------------------------------------------------------------------------

#school 

%%url: /api/school/show

function:
1. 显示查看所有 school

API:
正确的返回信息：
%%忽视用户登录信息


Info = {
	state: 0  Int # 0 表示成功，其他数字表示不成功
	message: ""   Char # 错误的提示信息
	data: {
		'all_countries' : [
			{
				'id' :   ~ Int 从0递增的数字，国家的index
	            'name' :  ~ int  国家的名字
	            'provs' : [
	            	{
	            		'country_id' :  ~  char 所属国家的id
		                'id' :  ~  int 省份的index， 从1递增
		                'name' :  ~  char  省份的名字
		                'univs' :  [ ~ 学校的名字
		                	{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},
		                	......
		                ]
	           		},{
	            		'country_id' :  ~  char 所属国家的id
		                'id' :  ~  int 省份的index， 从1递增
		                'name' :  ~  char  省份的名字
		                'univs' :  [ ~ 学校的名字
		                	{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},
		                	......
		                ]
	           		},
	           		......
	            	
	            ]
			},{
				'id' :   ~ Int 从0递增的数字，国家的index
	            'name' :  ~ int  国家的名字
	            'provs' : [
	            	{
	            		'country_id' :  ~  char 所属国家的id
		                'id' :  ~  int 省份的index， 从1递增
		                'name' :  ~  char  省份的名字
		                'univs' :  [ ~ 学校的名字
		                	{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},
		                	......
		                ]
	           		},{
	            		'country_id' :  ~  char 所属国家的id
		                'id' :  ~  int 省份的index， 从1递增
		                'name' :  ~  char  省份的名字
		                'univs' :  [ ~ 学校的名字
		                	{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},{
		                		'id' :  ~  int  省份的ID * 1000 +学校的index， 递增
			                    'name' :  ~  char 学校的名字
			                    'school_id' :  ~  char 学校的id，唯一表示
		                	},
		                	......
		                ]
	           		},
	           		......
	            	
	            ]
			},
			.......
			
		]
	}


-----------------------------------------------------------------------------------------------

#school 

%%url: /api/school/detail/{school_id}

function:
%%{school_id} 即为school的id，可以为空
1. 显示查看school的具体信息
2. 显示该school 下已经注册成功的host

API:
正确的返回信息：
%%忽视用户登录信息

Info = {
	state: 0   Int # 0 表示成功，其他数字表示不成功
	message: ''   Char # 错误的提示信息
	data: {
		'login_flag'  :  ~    int 用户的登录信息，已经登录为1，未登录为0
        
        'school'  : {
        	's_name' : ~  char 学校的名字= self.s_name
	        's_province' : ~  char 所属的省份
	        's_display_index' : ~  int 学校的index
	        's_student_number' : ~  = int 学校的host人数
        } 
        'allPeople'  :  ~   int  学校的host人数
        'topics'  : [
	        {
	        	'name' :  ~   char  学校的名字
	            'tag' :  ~   char  这个topic的标签（缩写）
	            'number' :  ~   int 这个topic下的host数量
	            'index' :  ~   从0递增
	            'hosts' :  {  ~ 每个host的信息
	            	'host_id_1' :1,
	            	'host_id_1' :1,
	            	'host_id_1' :1,
	            	....
	            }		
	        },{
	        	'name' :  ~   char  学校的名字
	            'tag' :  ~   char  这个topic的标签（缩写）
	            'number' :  ~   int 这个topic下的host数量
	            'index' :  ~   从0递增
	            'hosts' :  {  ~ 每个host的信息
	            	'host_id_1' :1,
	            	'host_id_1' :1,
	            	'host_id_1' :1,
	            	....
	            }		
	        },
	        .......
        ]
        'object'  :  [
        	{
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

				'tag' : ~ char 显示该用户的标签集合 用空格隔开
			},{
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

				'tag' : ~ char 显示该用户的标签集合 用空格隔开
			},
			.......
        	
        ]
	}




错误的返回信息：

Info = {
	state: 404   Int # 0 表示成功，其他数字表示不成功
	message: ‘找不到该学校’   Char # 错误的提示信息
	data: {}






-----------------------------------------------------------------------------------------------


注册用户第一步

url:   /account
method :POST

function :
1. 提交用户的姓名，手机号，邮箱，学历，本科学校、研究生学校，密码

API:
前段传输的数据字段

{
	username:    ~char  用户名
	email			~char 邮箱，前段验证
	phone			~ char 电话号码
	password			~密码
	password-confirm	~重新输入的密码，前后端均进行验证
	school1			~本科学校名字
	school2			~硕士学校	名字
	school3 		~博士学校名字
	schoolID1		~本科学校ID
	schoolID2		~硕士学校ID
	schoolID3		~博士学校ID
	education   	~int   0 表示本科， 1 表示研究生， 2 表示 博士生 ， 3 表示其他
}


如果注册成功，返回登陆页面，如果注册出错，返回注册

{
    'state': :  ~ int 类似于 404，如果为非零数即为出粗
    'message' : ~ char 出错信息
}





-----------------------------------------------------------------------------------------------
显示页面
url:/complete_account_feature/
method :GET

function :
1. 显示所有的topic 和topic下的minor topic
2. 如果用户在该minor topic 添加过feature，显示feature

API:

返回的数据格式：

data = {
	
    'login_flag' : True
    'user_features' : [
    	{
            'intro' :  ~ char 话题的介绍
            'name' : ~char 话题的名字
            'id' : ~ char 话题ID
            'tag' : ~ char 话题的小标签
            'feature_list': [
            	{
            		'f_name' :   ~ char feature 的名字 
	                'm_name' :   ~ char 小标题的名字
	                'f_id' :   ~ char feature 的ID
	                'm_id' :   ~ char 小标题的ID
            	},{
            		'f_name' :   ~ char feature 的名字 
	                'm_name' :   ~ char 小标题的名字
	                'f_id' :   ~ char feature 的ID
	                'm_id' :   ~ char 小标题的ID
            	},
            	......
            ]
            'minor_topic_list' : [
            	{
            		m_name :  ~ char 小话题的名字
				    m_topic :   ~ char 所属大话题的名字
				    m_introduction :  ~ char 小话题的介绍
            	},{
            		m_name :  ~ char 小话题的名字
				    m_topic :   ~ char 所属大话题的名字
				    m_introduction :  ~ char 小话题的介绍
            	},
            	....
            ]
    	},{
            'intro' :  ~ char 话题的介绍
            'name' : ~char 话题的名字
            'id' : ~ char 话题ID
            'tag' : ~ char 话题的小标签
            'feature_list': [
            	{
            		'f_name' :   ~ char feature 的名字 
	                'm_name' :   ~ char 小标题的名字
	                'f_id' :   ~ char feature 的ID
	                'm_id' :   ~ char 小标题的ID
            	},{
            		'f_name' :   ~ char feature 的名字 
	                'm_name' :   ~ char 小标题的名字
	                'f_id' :   ~ char feature 的ID
	                'm_id' :   ~ char 小标题的ID
            	},
            	......
            ]
            'minor_topic_list' : [
            	{
            		id :  char~  minor topic 的id
            		m_name :  ~ char 小话题的名字
				    m_topic :   ~ char 所属大话题的名字
				    m_introduction :  ~ char 小话题的介绍
            	},{
            		id :  char~  minor topic 的id
            		m_name :  ~ char 小话题的名字
				    m_topic :   ~ char 所属大话题的名字
				    m_introduction :  ~ char 小话题的介绍
            	},
            	....
            ]
    	},
    	......
    ]
	'host' = host,

}


-----------------------------------------------------------------------------------------------


添加feature

url:   /complete_account_feature/
method :POST

function :
1. 添加topic下的minor topic的feature
2. 如果发生feature 重复，额外输入，返回错误信息

API:

传输的数据

{
	'topic_id' : ~ topic的ID
    "feature_name" :  ~ feature 的名字

    "topic_tag"  :  ~ char  要在这个topic下添加的一个标识符
    "minor_topic_id" : ~ char 要添加的minor_topic 的ID
}


返回：

{

    'state' = 0
    'message' = "添加成功"
	'data' = {
		'topic_tag' :   ~ char  前段传过来的topic的小tag
		'topic_id' : ~ topic的ID
		'feature_name' :   ~ 添加的feature ID
		"m_id" : ~添加的 minor topic ID
	}
    

}



-----------------------------------------------------------------------------------------------


删除feature

url:   /delete-feature
method :POST

function :
1. 删除该用户的该TOPIC下的feature

API:

传输的数据

{
	'topic_id' : ~ topic的ID
    "feature_name" :  ~ feature 的名字
    "m_id" : ~添加的 minor topic ID
}


返回：

#查不到用户信息

Info = {
	state: 404   Int # 0 表示成功，其他数字表示不成功
	message: ‘找不到该用户’   Char # 错误的提示信息
	data: {}
}

#找不到该TOPIC，Feature 
Info = {
	state: 404   Int # 0 表示成功，其他数字表示不成功
	message: ‘删除失败，找不到该Topic或Feature’   Char # 错误的提示信息
	data: {}
}

#删除成功

Info = {
	state: 0   Int # 0 表示成功，其他数字表示不成功
	message: '删除成功'   Char # 错误的提示信息
	data: {
		"feature_name" :  ~ feature 的名字
        'topic_id'       ~    topic 的 id标识符
        'feature_name'       ~    feature 的名字
        'm_id'       ~    minor 的id标识符
        'f_id'       ~    feature的id 标识符
	}
}


-----------------------------------------------------------------------------------------------


搜索

url:   /general_search     ~给网页端用的
url:   /api/general_search     ~给app用的

method :GET

function :
1.  找查以下信息
	a).   “分享家”的一句话简介；
    b).   学校&专业；
    c).   咨询服务列表（“分享家”自定义输入的具体内容）；
    d).   前述咨询服务列表所涉及到的大话题&小话题；
    e).   详细的自我介绍；
2.返回结果是包含这两个关键字的用户列表，如果没有结果，提示前段/app

API:

提交的数据
{
	'word_1' :  ~char 关键字1
	'word_1' :  ~char 关键字2
}

返回数据

#有数据的情况

data = {
	state: 0   Int # 0 表示成功，其他数字表示不成功
	message: '删除成功'   Char # 错误的提示信息
	'search_result'  :  [
    	{
    		'id' : char  用户的唯一标识符
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

		},{
			'id' : char  用户的唯一标识符
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

		},
		.......       	
    ],
    'search_number'  ~int 找到host的个数
}









