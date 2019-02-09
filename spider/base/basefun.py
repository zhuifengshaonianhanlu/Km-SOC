#coding:utf-8

"""
Author:hanlu
"""

import requests,json,hashlib,configparser,datetime


class CONF():

    def __init__(self,conf_path):
        self.conf_path = conf_path

    def GET_CONF(self,section, option):
        '''
        获取指定section下指定key的value
        :param section: 
        :param option: 
        :return: 
        '''
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        so_value = config.get(section=section, option=option)
        return so_value

    def GET_CONF_items(self,section):
        '''
        获取指定section下的所有配置项
        :param section: 
        :return: [('key','value'),()]
        '''
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        section_items = config.items(section)
        return section_items

    def GET_CONF_SECTION_LIST(self,section_name):
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        section_list = config.options(section_name)
        return section_list

    def DEL_SECTION(self,section,key):
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        config.remove_option(section,key)
        config.write(open(conf_path, 'w'))
        return True

    def ADD_config_items(self,sectionname, key, values):
        config = configparser.ConfigParser()
        config.read(self.conf_path)
        if sectionname not in config.sections():
            config.add_section(sectionname)
        config.set(sectionname, key, values)
        config.write(open(self.conf_path, 'w'))

        section_keys = config.options(sectionname)
        # print(section_keys)
        return section_keys

