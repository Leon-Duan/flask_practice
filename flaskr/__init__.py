import os

from flask import Flask

def create_app(test_config=None):
    #创建app
    app = Flask(__name__, instance_relative_config=True)   # name是名字，后面表示添加一些内容给app吗，是的
    app.config.from_mapping(   #map 是映射，可以理解为字典，这里就是说默认传给app一些内容，是字典的形式，
                               #SECRET_KEY是密钥，DATABASE是数据库                              
        SECRET_KEY='dev',   
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #加载测试的内容，如果存在
        app.config.from_pyfile('config.py', silent=True)
    else:
        #加载测试配置
        app.config.from_mapping(test_config)
    
    #保证instance文件夹存在
    try:    os.makedirs(app.instance_path)
    except OSError:    pass

    #简单的初始页面
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)  #确保每次操作后关闭数据库连接

    return app
