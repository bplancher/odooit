OdooIT
======

Short presentation
------------------

OdooIT is a Python project where i put all the tools i developed to help me for Odoo modules development.
For now, this project contains:
* XMLRPC wrapper
* ...

An official RPC wrapper already exists (OdooRPC), but i wanted a more advanced implementation of some Odoo aspects, such as seeing the workflow state of an object, 'ping' databases after a server restart, etc... 

This project is a new-born one, it only stores my current tools 'as it', so it may lacks some documentation or examples.
But i will try to improve this ASAP.

### XMLRPC wrapper (OdooITRPC)

This object requires some classic information to be usable:
* host (including the port), for example: http://localhost:8069
* database name
* login
* password

Once these informations are set, you can call every ORM methods by directly using the method name (as the old browse_record does).

#### Documentation

**OdooITRPC: (host, db, username, password, [debug])**
* host: (string) the Odoo instance url, including the port
* db: (string) the database name you want to query
* username: (string) a valid login user (or whatever authenticated method handled by your Odoo instance, such as ldap, etc...)
* password: (string) a valid password for the given login
* debug: (boolean) optional, if True, will print all xmlrpc calls with their execution time

The constructor: it tries to authenticate to the instance using the information you gave.

**load(model)**
* model: (string) the ORM model (with 'dot' synthax) you want to query)
* returns: self, so you can chain with a call to the ORM

**ping_db()**
No argument, it only lists existing Odoo databases, and perform a 'fake' login with credentials login:'ping', password: 'ping'.

The only goal of this method is to force Odoo to initialize all of its instances. For example, after restarting Odoo server without precising any database (this avoid some issues when using Web API, for custom UI or other purposes).

**other_method_names(*args, **kwargs)**
For any other methods, the object will execute the following command (as you would do with pure xmlrpclib call):

xmlrpc_server.execute_kw(db, uid, password, model, method_name, args, kwargs)

#### Example:

	from odooit import OdooITRPC

	# initialize the object
	host = 'http://localhost:8069'
	db = 'odoo'
	user = 'user'
	pwd = 'password'
	sock = OdooITRPC(host, db, user, pwd, debug=True)
	# the constructor did the authentication step, the object is now usable
	# before doing anything else, you NEED to call load() method
	# then, call whatever public ORM method available on the loaded model
	# this internally calls execute_kw(db, uid, pwd, 'res.users', 'context_get', [], {})
	context = sock.load('res.users).context_get()
	# this internally calls execute_kw(db, uid, pwd, 'res.users', 'read', [[]], {'context': context})
	user_infos = sock.read(sock.uid, [], context=context)
	print user_infos.get('name', '')
	# >> u'username'

