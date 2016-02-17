# -*- coding: utf-8 -*-

# author: Bruno PLANCHER
# company: atReal Ouest

import xmlrpclib
import time


class OdooITRPC(object):
    def __init__(self, env, db, user, pwd, debug=False):
        self.env = env
        self.db = db
        self.user = user
        self.pwd = pwd
        self.debug = debug
        self.model = False
        self.get_connection_infos()

    def get_wkf_state(self, model, ids):
        ids = ids if isinstance(ids, list) else [ids]
        ret_ids = self.load('workflow.workitem').search([('inst_id.res_id', 'in', ids),
                                                    ('inst_id.res_type', '=', model)])
        ret = self.read(ret_ids, [])
        for item in ret:
            print item
        return ret

    def get_email_preview(self, record_id, template_id):
        self.load('email_template.preview')
        ret = self.on_change_res_id(False, record_id, {'template_id': template_id})
        return ret['value']['body_html']

    def get_connection_infos(self):
        self.host = self.env
        self.sock_common = xmlrpclib.ServerProxy(self.host + '/xmlrpc/common')
        self.sock_db = xmlrpclib.ServerProxy(self.host + '/xmlrpc/db')
        self.uid = self.sock_common.login(self.db, self.user, self.pwd)
        self.sock = xmlrpclib.ServerProxy(self.host + '/xmlrpc/object')

    def load(self, model):
        self.model = model
        return self

    def ping_db(self):
        dbnames = self.sock_db.list()
        for db in dbnames:
            print 'ping db %s on %s' % (db, self.host)
            self.sock_common.login(self.db, 'ping', 'ping')

    def execute(self, model, method, *args, **kwargs):
        current_time = time.time()
        if self.debug:
            args_str = ','.join([str(x) for x in args]) if args else ''
            kwargs_str = ','.join(['%s= %s' % (x, kwargs.get(x)) for x in kwargs.keys()]) if kwargs else ''
            print '[%s] executing "%s(%s,%s)"' % (model, method, args_str, kwargs_str)
        ret = self.sock.execute_kw(self.db, self.uid, self.pwd, model, method, args, kwargs)
        if self.debug:
            print 'Done in %s sec' % str(time.time() - current_time)
        return ret

    def call(self, method, *args, **kwargs):
        assert self.model, 'Error: You have not loaded any model, use load() method before calling call()'
        return self.execute(self.model, method, *args, **kwargs)

    # if calls unidentified attribute, we suppose an xmlrpc call is expected
    def __getattr__(self, name):
        if name not in self.__dict__.keys():
            def func_proxy(*args, **kwargs):
                return self.call(name, *args, **kwargs)
            return func_proxy
        return self.__dict__.get(name)
