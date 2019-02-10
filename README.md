# Km-SOC

一个可以扩展的github源码监控系统

如果你想扩展，Km-SOC可以支持你把一些其他安全模块加入进去，比如：安全监控，扫描等。因此该系统命名为“Km-SOC”，其中的SOC正是此意。
（考虑到每个组织在SOC这一方面的需求和功能不一样，因此这一部分就不开源了）

说实在的，github源码监控的系统开源的很多，但老衲看来，写的都不行。
倒不是技术问题，我觉得主要是没有站在“安全运营”的角度来进行思考和设计。

在我看来github源码监控系统主要的目的只有一个，干脆而清晰，那就是：
尽可能全面的，及时的，发现与组织敏感信息相关的源码是否出现在github上

**所以这里有几个重点：**

1. 全面的:不管是使用纯爬虫的方式爬网页内容，还是使用github-API进行结果搜索，其都会受到github的“风控”限制，其中有一个限制是每次搜索请求最多提供1000条结果记录，也就是1000条以外会被遗漏掉。因此，如何全面的搜索与指定信息相关的内容，是一个必须要考虑的地方。

2. 及时的：这个没啥好说的，周期性的全github搜索即可，确保这个周期在可接受的范围同时又不触发github风控规则即可。

3. 敏感信息：需要定义好，什么样的信息是敏感信息。在github这样的场景中，不管是什么公司，至少有如下几点需要包含在敏感信息的范围内：


- 与组织相关的代码，同时又包含了组织比较敏感的信息，比如数据库连接串，秘钥，证书信息等。
- 与组织相关的代码，不包含以上敏感信息，但属于公司业务代码，泄露了公司的业务逻辑
- 与组织相关的代码，属于纯前端代码，比如html,css,javascript，因为这些代码本身是通过浏览器向外部开放的，因此是否定义为敏感信息，请根据公司安全管理要求进行定义，需要考虑的是，这些代码可能会特别多，会给结果造成大量的干扰，因此如何处理这种情况，也是需要考虑的


简单列一下github的限制，其中比较重要的是：

*1.To satisfy that need, the GitHub Search API provides up to 1,000 results for each search. //每次搜索请求最多提供1000条结果*

*2.The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, you can make up to 30 requests per minute //认证后的请求每分钟最多30次*

*3.不能将下列通配符用作搜索查询的一部分，：；/\‘“=！？#$&+^~<>(){}...。搜索将忽略这些符号*

*4.只有小于384 KB的文件可以搜索*

*5.最多，搜索结果可以显示来自同一个文件的两个片段，但是文件中可能有更多的结果。*

**在这些规则下，为了尽可能全面的，准确的找到“有风险”的告警，设计思路如下：**

1. 管理员提供需要搜索的keyword,keyword可以是多个 //keyword表示目标关键字，但不代表风险关键词，比如你要搜索“cisco”的泄露，keyword应该是：“cisco.com”,“思科”等关键字，keyword的意义是为了找到与组织相关的代码。

2. 管理员指定需要搜索的开发语言 //设计这一条的原因是：github上获取的结果中有大量的是html,css,javascript这些前端代码，由于api接口数量的限制，这些不大可能出现敏感信息的前端代码(从特性上前端代码本来就是开放给外面的)会占总数的很大一部分比例，同时结合公司实际开发技术栈指定需要搜索的后端语言，比如：java,php,go,python会更加准确。同时'Jupyter Notebook'，'Tex','JSON'等也应该在搜索范围内。

3. 根据“keyword+语言”找到所有结果，并得到结果里面所有的项目，既得到所有项目名称(repositories name)，以list方式返回。

4. 管理员指定有风险的payload,比如："password","mysql"，“accesskey”等。

5. 依次在第3步得到的所有项目中去搜索payload,命中的记录入库进行记录。

6. 以结果文件hash值为主键进行去重。

7. 为了更加有效率的扫描和有效的逃避githu风控规则，支持使用多个token进行扫描，建议配置至少≥2个以上token（spider/config/conf.ini中spider的token选项）



截几张图：(如果加载不出来，点一下可以单独打开)
登录界面：
</br>
![image](http://github.com/zhuifengshaonianhanlu/Km-SOC/tree/master/images/login.png)
</br>

用户管理界面：

![image](http://github.com/zhuifengshaonianhanlu/Km-SOC/tree/master/images/user.png)
</br>
配置管理界面：所有的配置可以在这里添加

![image](http://github.com/zhuifengshaonianhanlu/Km-SOC/tree/master/images/conf.png)
</br>
结果展示-1：所有命中了keyword的项目都会在这里列出来，可以在这里添加白名单（白名单里面的项目下次不会扫描）

![image](http://github.com/zhuifengshaonianhanlu/Km-SOC/tree/master/images/rs-1.png)
</br>
结果展示-2：这里详细显示了搜索的结果，同时会按照文件类型进行统计展示，点击某个问价类型，可以单独显示该类型所有的搜索结果。
同时，点击payload,会仅显示该payload的结果。

![image](http://github.com/zhuifengshaonianhanlu/Km-SOC/tree/master/images/rs-2.png)
</br>

python项目，用到的框架为Flask,数据库为mysql。

**下面是一个简单的部署指导：**

app---前端web和flask api接口

web.py---web服务启动主程序

spider---github搜索主程序


1.app/setting.py,前端配置文件，需要指定数据库连接串配置。请先创建好数据库。

2.spider/config/conf.ini,搜索程序配置文件，主要指定数据库连接串，github的token,spidier里面的配置可以通过soc界面进行配置，也可以在这里手动配置。

3.启动爬虫程序：python /spider/spider.py

4.启动web服务：python web.py

5.入口：http://127.0.0.1:5000/login



**而对于最开始说的扩展性，主要指的是：**

1.所有的api都是使用blueprint进行模块化注册的，在app/__init__.py的register_blueprint（）函数中进行注册即可。


2.web界面中左边的功能列表可以在lay.html中进行添加。







