# Km-SOC
github源码监控系统

说实在的，github源码监控的系统开源的很多，但老夫看来，写的都不行。
倒不是技术问题，我觉得主要是没有站在“安全运营”的角度来进行思考和设计。

在我看来github源码监控系统主要的目的只有一个，干脆和清晰，那就是：
尽可能全面的，及时的，发现与组织敏感信息相关的源码是否出现在github上

所以这里有几个重点：
1.全面的:不管是使用纯爬虫的方式爬网页内容，还是使用github-API进行结果搜索，其都会受到github的“风控”限制

github的限制：
1.To satisfy that need, the GitHub Search API provides up to 1,000 results for each search. //每次搜索请求最多提供1000条结果
2.The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, you can make up to 30 requests per minute //认证后的请求每分钟最多30次
3.

为了尽可能全面的，准确的找到“有风险”的告警，设计思路如下：
1.管理员提供需要搜索的keyword,keyword可以是多个 //keyword表示目标关键字，但不代表风险关键词，比如你要搜索海风教育的泄露，keyword应该是：“hfjy.com”,“hfjy”,“海风教育”等
2.管理员指定需要搜索的开发语言 //设计这一条的原因是：github上获取的结果中有大量的是html,css,javascript这些前端代码，由于api接口数量的限制，这些不大可能出现敏感信息的前端代码(从特性上前端代码本来就是开放给外面的)会占总数的很大一部分比例，同时结合公司实际开发技术栈指定需要搜索的后端语言，比如：java,php,go,python会更加准确。同时'Jupyter Notebook'，'Tex','JSON'等也应该在搜索范围内。
3.根据“keyword+语言”找到所有结果，总结出结果里面所有的项目名称(repositories)
4.管理员指定有风险的payload,比如："password","mysql"，“accesskey”等。
5.在第3步得到的所有项目中去搜索payload,命中的记录入库进行记录。
6.以结果hash值为主键进行去重
