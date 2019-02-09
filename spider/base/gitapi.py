#coding:utf-8

"""
Author:hanlu
"""
import requests,json,time,base64,random

class gitSearch():

    def __init__(self,tokenlist):
        token = random.sample(tokenlist,1)[0]

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3.text-match+json'}

    def search_code_req(self,keyword,language,page=1):
        '''
        search code in all github where q = keyword,and every page 100,default start page=1
        '''
        search_code_url = f"https://api.github.com/search/code?q={keyword}:language:{language}&page={page}&per_page=100&sort=updated"
        res = requests.get(search_code_url, headers=self.headers)
        resp = res.json()
        # print(resp)
        return resp

    def search_repo_code_req(self,payload,project,page=1):
        '''
        search code in one repo where q = payload,and every page 100,default start page =1
        '''
        search_code_url = f"https://api.github.com/search/code?&page={page}&per_page=100&q={payload}+repo:{project}"
        res = requests.get(search_code_url, headers=self.headers)
        resp = res.json()
        return resp



    def get_project_list(self,pages,keyword,language):
        """
        :param pages: 总页码
        :return: 
        """
        projects_list = []
        for page in range(1,pages):
            resp = self.search_code_req(keyword,language,page)

            result = resp.get('items')
            if result is None:
                return []

            for f in result:
                full_name = f['repository']['full_name']
                if full_name not in projects_list:
                    projects_list.append(full_name)
        return projects_list

    def get_searchCode_pages(self,target_s,keyword,language):
        tem_total_count = self.search_code_req(keyword,language)
        tem_total_count = tem_total_count.get('total_count')
        if tem_total_count is None:
            return None
        if tem_total_count == 0:
            return 0
        if target_s >= tem_total_count and tem_total_count <= 1000:
            target_s = tem_total_count
        if tem_total_count > 1000:
            target_s = 1000
        pages = target_s // 100 + 1 if (target_s % 100) == 0 else target_s // 100 + 2
        return pages

    def get_searchRepo_pages(self,payload,projectName):
        tem_total_count = self.search_repo_code_req(payload,projectName)
        tem_total_count = tem_total_count.get('total_count')
        #异常处理，由于gitapi风控，可能出现None
        if tem_total_count is None:
            return None
        if tem_total_count == 0:
            return 0
        target_s = tem_total_count if tem_total_count <= 1000 else 1000
        pages = target_s // 100 + 1 if (target_s % 100) == 0 else target_s // 100 + 2
        return pages
