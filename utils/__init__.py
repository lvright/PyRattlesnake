from .base import *

# TODO 初始化工具类
par_type = ParType()
wide_time = WideTime()
jwt_token = JsonWebToken()
captcha = Captcha()
http = Response()
tackle = Tackle()
data_base = DataBase()
db = DataBase().db_session()
log = Log()
manager = ConnectionManager()

# TODO 项目路径
project_file_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/PyRattlesnake'
