#coding:utf-8

import datetime,random,base64,time
from flask import Blueprint,render_template,request,redirect,url_for,flash,jsonify,session
from flask_login import login_user, logout_user, current_user, login_required,UserMixin,login_manager

from app.forms.formcheck import AddUserForm,LoginForm
from app.models.kmeye import KmResult,KmWhitelist
from app.models.base import db
from spider.base.basefun import CONF

kmeye = Blueprint('kmeye',__name__)


@kmeye.route('/kmrs',methods=['GET'])
@login_required
def kmrs():

    total_projcets = KmResult.query.with_entities(KmResult.owner,KmResult.pname).distinct().count()
    NoConfirm_projects = KmResult.query.with_entities(KmResult.purl).filter_by(confirm=0).distinct().count()
    # Payload_projects = KmResult.query.with_entities(KmResult.purl).filter(payload!='Null').distinct().count()
    # Payload_projects = KmResult.query.with_entities(KmResult.purl).filter(KmResult.payload != None).distinct().count()
    confirm_projects = total_projcets - NoConfirm_projects
    return render_template('kmeye/result.html',total_projcets=total_projcets,NoConfirm_projects=NoConfirm_projects,confirm_projects=confirm_projects)


@kmeye.route('/kmrs/pageinfo',methods=['GET'])
@login_required
def pageinfo():
    per_page = 15
    resp = KmResult.query.with_entities(KmResult.owner, KmResult.pname, KmResult.purl).distinct().paginate(page=1,per_page=per_page,error_out=True)
    total_page = resp.pages
    return jsonify({'total_page':total_page})

@kmeye.route('/kmrs/<int:page>',methods=['GET'])
@login_required
def km_result(page):
    """
    page //表示第几页
    per_page //每页显示多少条数据
    :return:
    """
    per_page = 15
    # resp = KmResult.query.filter_by(confirm=0).paginate(page=page, per_page=per_page, error_out=True)
    resp = KmResult.query.with_entities(KmResult.source,KmResult.owner,KmResult.pname,KmResult.purl).distinct().paginate(page=page, per_page=per_page, error_out=True)

    # whitelist = []
    # wl = KmWhitelist.query.with_entities(KmWhitelist.purl).all()
    # for w in wl:
    #     whitelist.append(w[0])

    total_page = resp.pages
    result_items = resp.items
    result_list = []
    for i in result_items:
        purl = i.purl
        source = i.source
        owner = i.owner
        pname = i.pname
        #判断是否还存在未确认的项目：
        confirm_data = KmResult.query.filter_by(purl=purl,confirm=0).first()
        confirm = 0 if confirm_data else 1

        rs = {'source':source,'owner':owner,'pname':pname,'purl':purl,'confirmv':confirm}
        result_list.append(rs)

    return jsonify({'result':result_list,'total_page':total_page}),200


@kmeye.route('/kmrs/detail/<owner>/<pname>',methods=['GET'])
@login_required
def detail(owner,pname):

    try:
        purl_t = KmResult.query.with_entities(KmResult.purl).filter_by(owner=owner,pname=pname).distinct().first()
        purl = purl_t.purl

        payload_list = []
        payload_t = KmResult.query.with_entities(KmResult.payload).filter_by(owner=owner,pname=pname).distinct().all()
        for p in payload_t:
            if p[0]:
                payload_list.append(p[0])


        keyword_list = []
        keyword_t = KmResult.query.with_entities(KmResult.keyword).filter_by(owner=owner,pname=pname).distinct().all()
        for k in keyword_t:
            keyword_list.append(k[0])

        btnlist = ['btn', 'btn btn-success', 'btn btn-warning', 'btn btn-primary', 'btn btn-inverse', 'btn btn-pink','btn btn-purple','btn btn-yellow']
        filetype_list = []
        filetype_t = KmResult.query.with_entities(KmResult.filetype).filter_by(owner=owner,pname=pname).distinct().all()
        for f in filetype_t:
            btn = random.sample(btnlist, 1)
            filetype_count = KmResult.query.filter_by(owner=owner,pname=pname,filetype=f[0]).count()
            rs = {'filetype':f[0],'count':filetype_count,'btn':btn[0]}
            filetype_list.append(rs)

        resp = KmResult.query.filter_by(owner=owner,pname=pname).all()
        result_items = resp
        result_list = []
        for i in result_items:
            if not i.filename:
                continue
            content = i.content
            if content:
                content = base64.b64decode(content).decode()

            note = i.note
            if not note:
                note = 'no comments~'

            rs = {'filename':i.filename,'fileurl':i.fileurl,'content':content,'confirm':i.confirm,'filehash':i.filehash,'note':note}
            result_list.append(rs)

    except BaseException as e:
        flash('参数异常')
        return render_template('kmeye/detail.html',owner=owner, pname=pname, purl=purl)
    else:
        return render_template('kmeye/detail.html', owner=owner, pname=pname, purl=purl, result=result_list,
                               keyword=keyword_list,
                               payload=payload_list, filetype=filetype_list)


@kmeye.route('/kmpd/<owner>/<pname>/<payload>')
@login_required
def kmpd(owner,pname,payload):
    resp = KmResult.query.filter_by(owner=owner, pname=pname,payload=payload).all()
    result_items = resp
    result_list = []
    for i in result_items:
        content_t = i.content
        content = base64.b64decode(content_t).decode()

        note = i.note
        if not note:
            note = 'no comments~'

        rs = {'filename': i.filename, 'fileurl': i.fileurl, 'contentv': content, 'confirmv': i.confirm,'filehash':i.filehash,'note':note}
        result_list.append(rs)
    return jsonify({'result':result_list}),200



@kmeye.route('/kmft/<owner>/<pname>/<filetype>')
@login_required
def kmft(owner,pname,filetype):
    resp = KmResult.query.filter_by(owner=owner, pname=pname,filetype=filetype).all()
    result_items = resp
    result_list = []
    for i in result_items:
        content_t = i.content
        content = base64.b64decode(content_t).decode()

        note = i.note
        if not note:
            note = 'no comments~'

        rs = {'filename': i.filename, 'fileurl': i.fileurl, 'contentv': content, 'confirmv': i.confirm,'filehash':i.filehash,'note':note}
        result_list.append(rs)
    return jsonify({'result':result_list}),200


@kmeye.route('/kmconfirm/<filehash>')
@login_required
def kmconfirm(filehash):
    try:
        article_data = KmResult.query.filter(KmResult.filehash == filehash).first()
        article_data.confirm = 1
        db.session.commit()
    except BaseException as e:
        return jsonify({'result':'error'}),401
    else:return jsonify({'result':'ok'}),200


@kmeye.route('/kmall/<owner>/<pname>/<filetype>')
@login_required
def kmall(owner,pname,filetype):
    try:
        article_data = KmResult.query.filter(KmResult.owner == owner,KmResult.pname == pname,KmResult.filetype == filetype).all()
        for a in article_data:
            a.confirm = 1
        db.session.commit()
    except BaseException as e:
        return jsonify({'result':'error'}),401
    else:return jsonify({'result':'ok'})


@kmeye.route('/kmnote/<filehash>',methods=['GET','POST'])
@login_required
def kmnote(filehash):
    try:
        note_data = request.get_json()
        article_data = KmResult.query.filter(KmResult.filehash == filehash).first()
        article_data.note = note_data['note']
        db.session.commit()
    except BaseException as e:
        return jsonify({'result':'error'}),401
    else:return jsonify({'result':'ok'}),200


@kmeye.route('/kmaddwl' ,methods=['GET','POST'])
@login_required
def kdaddwl():
    try:
        wl_data = request.get_json()
        eventtime = time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(time.time()))
        wl_info = KmWhitelist(eventtime=eventtime,owner=wl_data['owner'],pname=wl_data['pname'],purl=wl_data['purl'])
        db.session.merge(wl_info)

        KmResult.query.filter_by(purl=wl_data['purl']).delete()
        db.session.commit()

    except BaseException as e:
        return jsonify({'result':'error'}),401
    else:return jsonify({'result':'ok'}),200


'''
监控配置接口
'''
cf = CONF('spider/config/conf.ini')

@kmeye.route('/kmcf',methods=['GET'])
@login_required
def kmcf():
    keyword = cf.GET_CONF('spider','keyword').split(',')
    payload = cf.GET_CONF('spider','payload').split(',')
    language = cf.GET_CONF('spider','language').split(',')
    target = cf.GET_CONF('spider','target')

    rox = KmWhitelist.query.all()
    wlist = []
    for k in rox:
        wtime = k.eventtime
        owner = k.owner
        pname = k.pname
        purl = k.purl
        rs = {'wtime':wtime,'owner':owner,'pname':pname,'purl':purl}
        wlist.append(rs)


    wltotal = len(wlist)
    return render_template('kmeye/kmcf.html',keyword=keyword,payload=payload,language=language,target=target,wlist=wlist,wltotal=wltotal)


@kmeye.route('/delkey',methods=['POST'])
@login_required
def delkey():
    try:
        del_data = request.get_json()
        del_type = del_data['type']

        if del_type in ['keyword','payload','language']:
            del_key = del_data['key']
            old_conflist = cf.GET_CONF('spider',del_type).split(',')

            old_conflist.remove(del_key)
            new_confstr = ','.join(old_conflist)
            cf.ADD_config_items('spider', del_type, new_confstr)
        else:jsonify({'result': 'error'}), 401


    except BaseException as e:
        return jsonify({'result': 'error'}), 401
    else:
        return jsonify({'result': 'ok'}), 200

@kmeye.route('/kmaddconf',methods=['POST'])
@login_required
def kmaddconf():
    try:
        conf_data = request.get_json()
        conf_type = conf_data['type']
        if conf_data.get('conf') == '':
            return jsonify({'result':'内容不能为空'}),200

        if conf_type == 'target':
            cf.ADD_config_items('spider',conf_type,conf_data['conf'])

        if conf_type in ['keyword','payload','language']:
            conf = conf_data['conf']
            add_conflist = conf.split(',')

            old_conflist = cf.GET_CONF('spider',conf_type).split(',')

            new_conflist = add_conflist if not old_conflist[0] else list(set(add_conflist+old_conflist))
            new_confstr = ','.join(new_conflist)
            cf.ADD_config_items('spider',conf_type,new_confstr)

    except BaseException as e:
        return jsonify({'result':'请求异常'})
    else:return jsonify({'result':'添加成功'}),200

@kmeye.route('/kmdelwl',methods=['POST'])
@login_required
def kwdelwl():
    try:
        del_data = request.get_json()
        KmWhitelist.query.filter_by(purl=del_data['purl']).delete()
    except BaseException as e:
        return jsonify({'result': 'error'}), 401
    else:return jsonify({'result': 'ok'}), 200


