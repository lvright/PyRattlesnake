from .base import *

# TODO 初始化工具类
par_type = ParType()
wide_time = WideTime()
jwt_token = JsonWebToken()
captcha = Captcha()
http = ResponseMethod()
tackle = Tackle()
data_base = DataBase()
db = DataBase().session
log = Log()
manager = ConnectionManager()
base_code = BaseCode()

# TODO 项目路径
project_file_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/PyRattlesnake'

# TODO 当前时间和时间戳
now_date_time = str(datetime.now().strftime('%Y-%m-%d %H:%m'))
now_timestamp = int(time.time())
