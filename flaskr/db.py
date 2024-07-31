import sqlite3

import click
from flask import current_app, g  

def get_db():
    if 'db' not in g:    # 使用get_db()函数将db传给g
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  #g里面的db的路径
            detect_types=sqlite3.PARSE_DECLTYPES   # 启用sqlite3的日期时间类型
        )
        g.db.row_factory = sqlite3.Row

    return g.db   #传送完毕

def close_db(e=None):    # 说明下，第一段代码就是说，将g字典中的db键的值赋给db变量，然后删除g字典中的db键，如果没有该键，则返回None，e代表错误，这里默认=none就是强制没有错误，即一定要关闭
    db = g.pop('db', None)

    if db is not None:       
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:    # 读取schema.sql文件
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')  #格式化数据库
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) #出现teardown_appcontext，说明在每次请求结束后都会调用这个函数，关闭数据库连接
    app.cli.add_command(init_db_command)  #牛逼 在命令行添加命令