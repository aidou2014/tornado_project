from sqlalchemy import create_engine  # 导入
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接参数
USERNAME = 'root'
PASSWORD = 'qwe123'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'

Db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

engine = create_engine(Db_url)  # 连接数据库
Base = declarative_base(engine)  # 建模来使用继承来建立基类
Session = sessionmaker(engine)  # 生成一个会话类，用来操作数据的
session = Session()
