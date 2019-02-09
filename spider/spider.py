#coding:utf-8

"""
Author:hanlu
github api limited:
1.To satisfy that need, the GitHub Search API provides up to 1,000 results for each search.
2.The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, you can make up to 30 requests per minute
"""

import time,base64,random
from apscheduler.schedulers.blocking import BlockingScheduler
from base.logger import PrintLog
from base.basefun import CONF
from base.gitapi import gitSearch
from base.dbclass import *

logfilename = 'log/kmeye.log'
logger = PrintLog(logfilename)
conf = CONF('config/conf.ini')

username = conf.GET_CONF('database','username')
password = conf.GET_CONF('database','password')
host = conf.GET_CONF('database','host')
port = conf.GET_CONF('database','port')
dbname = conf.GET_CONF('database','dbname')
db_path = f"mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8"
connect = create_engine(db_path,echo=False,pool_size=30)
Base.metadata.create_all(connect)

tokenlist = conf.GET_CONF('github', 'token').split(',')
keywords = conf.GET_CONF('spider','keyword').split(',')
payloads = conf.GET_CONF('spider','payload').split(',')
languages = conf.GET_CONF('spider','language').split(',')
targets = int(conf.GET_CONF('spider','target'))
whitelist = get_wlist(connect)


def start_spider():
    for language in languages:
        gS = gitSearch(tokenlist)
        # print(gS.headers)

        for keyword in keywords:
            pages = gS.get_searchCode_pages(targets,keyword,language=language)
            if pages is None:
                continue
            if pages == 0:
                logger.info(f'没有搜索到符合-{keyword}-的内容')
                continue
            projects = gS.get_project_list(pages,keyword,language=language)

            for payload in payloads:
                for projectName in projects:
                    if projectName in whitelist:
                        continue
                    owner = projectName.split('/')[0]
                    pname = projectName.split('/')[1]
                    purl = f'https://github.com/{projectName}'
                    confirm = 0
                    source = 'GITHUB'

                    pages = gS.get_searchRepo_pages(payload, projectName)
                    if pages is None:
                        continue
                    if pages == 0:
                        # 仅命中了keyword,但是没有命中payload:
                        eventtime = time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(time.time()))
                        filehash = str(projectName) + '/' + str(payload)
                        # print({'msg': f'{projectName}中未发现{payload}'})
                        merge_result(connect,
                                     eventtime=eventtime,
                                     owner=owner,
                                     pname=pname,
                                     purl=purl,
                                     filehash=filehash,
                                     confirm=confirm,
                                     source=source,
                                     keyword=keyword)
                        continue
                    for page in range(1, pages):
                        #此处重新初始化gS这个类，从新随机获取一个token
                        gS = gitSearch(tokenlist)
                        # print(gS.headers)
                        tmp_result = gS.search_repo_code_req(payload, projectName, page)
                        items = tmp_result.get('items')

                        if tmp_result.get('message'):
                            time.sleep(60)
                            tmp_result = gS.search_repo_code_req(payload, projectName, page)
                            items = tmp_result.get('items')

                        for i in items:
                            eventtime = time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(time.time()))
                            filename = i.get('name')
                            filehash = i.get('sha')
                            filetype = filename.split('.')[-1] if '.' in filename else 'unknow'
                            fileurl = i.get('html_url')
                            text_matches = i.get('text_matches')
                            for text in text_matches:
                                part = text['fragment']
                                part_base64 = base64.b64encode(part.encode('utf-8'))
                                content = str(part_base64, 'utf-8')
                                merge_result(connect,
                                             eventtime=eventtime,
                                             owner=owner,
                                             pname=pname,
                                             purl=purl,
                                             filename=filename,
                                             filehash=filehash,
                                             fileurl=fileurl,
                                             filetype=filetype,
                                             confirm=confirm,
                                             source=source,
                                             keyword=keyword,
                                             payload=payload,
                                             content=content)
                    time.sleep(30)



if __name__ == '__main__':

    # start_spider()

    """
    每x个小时运行一次
    seconds
    minutes
    hours
    """

    sched = BlockingScheduler()
    sched.add_job(start_spider, 'interval', hours=2)
    sched.start()






