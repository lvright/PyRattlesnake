# -*- coding: utf-8 -*-


accountData = [
    {
        "id": 1,
        "username": "superAdmin",
        "avatar": "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwx1.sinaimg.cn%2Flarge%2F006APoFYly8gu2q67x7h7g30dc0dc0u0.gif&refer=http%3A%2F%2Fwx1.sinaimg.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1660900043&t=a0e3b7e7ddc0e89bd6d0eafbc27ff8a5",
        "userId": "superAdmin",
        "password": "888888",
        "user_type": "100",
        "nickname": "蟒蛇大师",
        "phone": "16858888988",
        "email": "admin@py.com",
        "dashboard": "statistics",
        "status": "1",
    },
]

settingData = [
    {
        "mode": "light",
        "tag": "1",
        "menuCollapse": "0",
        "menuWidth": 240,
        "layout": "classic",
        "skin": "mine",
        "language": "zh_CN",
        "color": "",
        "user_id": 1
    }
]

extendData = [
    {
        "group_name": "extend",
        "name": "网站是否关闭",
        "key": "web_close",
        "isVirtual": "1",
        "isSet": "0",
        "value": "1",
        "sort": 0,
        "remark": "关闭网站后将无法访问"
    },
    {
        "group_name": "extend",
        "name": "后台登录验证码方式",
        "key": "web_login_verify",
        "isVirtual": "1",
        "isSet": "0",
        "value": "0",
        "sort": 0,
        "remark": "0 前端验证，1 后端验证"
    }
]

configData = [
    {
        "group_name": "system",
        "name": "网站名称",
        "key": "site_name",
        "value": "",
        "sort": 99,
        "remark": ""
    },
    {
        "group_name": "system",
        "name": "网站关键字",
        "key": "site_keywords",
        "value": "",
        "sort": 98,
        "remark": ""
    },
    {
        "group_name": "system",
        "name": "网站描述",
        "key": "site_desc",
        "value": "",
        "sort": 97,
        "remark": ""
    },
    {
        "group_name": "system",
        "name": "版权信息",
        "key": "site_copyright",
        "value": "",
        "sort": 96,
        "remark": ""
    },
    {
        "group_name": "system",
        "name": "网站备案号",
        "key": "site_record_number",
        "value": "",
        "sort": 95,
        "remark": ""
    },
    {
        "group_name": "system",
        "name": "上传存储模式",
        "key": "site_storage_mode",
        "value": "local",
        "sort": 93,
        "remark": ""
    }
]

postData = [
    {
        "id": 1,
        "name": "产品主管",
        "code": "pmm",
        "sort": 19,
        "status": "1",
        "remark": ""
    },
    {
        "id": 2,
        "name": "技术主管",
        "code": "pmm",
        "sort": 20,
        "status": "1",
        "remark": ""
    }
]

deptData = [
    {
        "id": 1,
        "parent_id": 0,
        "level": "0",
        "name": "蟒蛇科技",
        "phone": "16888888888",
        "status": "1",
        "sort": 0,
        "remark": "",
    },
    {
        "id": 2,
        "parent_id": 1,
        "level": "0",
        "name": "产品部",
        "phone": "16888888888",
        "status": "1",
        "sort": 0,
        "remark": "",
    },
    {
        "id": 3,
        "parent_id": 1,
        "level": "0",
        "name": "研发部",
        "phone": "16888888888",
        "status": "1",
        "sort": 0,
        "remark": "",
    }
]

roleData = [
    {
        "id": 1,
        "name": "超级管理员",
        "code": "superAdmin",
        "data_scope": "1",
        "dept_ids": "",
        "sort": "0",
        "status": "1"
    },
    {
        "id": 2,
        "name": "测试角色",
        "code": "testAdmin",
        "data_scope": "2",
        "dept_ids": "1,2,3",
        "sort": "0",
        "status": "1"
    }
]

roleRelationData = [
    {
        "id": 1,
        "user_id": 1,
        "role_id": 1
    }
]

postRelationData = [
    {
        "id": 1,
        "user_id": 1,
        "post_id": 1
    },
    {
        "id": 2,
        "user_id": 1,
        "post_id": 2
    }
]

deptRelationData = [
    {
        "id": 1,
        "user_id": 1,
        "dept_id": 1
    }
]

dictTypeData = [
    {
        "id": 1,
        "name": "数据表引擎",
        "code": "table_engine",
        "status": "1",
        "remark": "数据表引擎字典"
    },
    {
        "id": 2,
        "name": "存储模式",
        "code": "upload_mode",
        "status": "1",
        "remark": "上传文件存储模式"
    },
    {
        "id": 3,
        "name": "数据状态",
        "code": "data_status",
        "status": "1",
        "remark": "通用数据状态"
    },
    {
        "id": 4,
        "name": "后台首页",
        "code": "dashboard",
        "status": "1",
        "remark": ""
    },
    {
        "id": 5,
        "name": "性别",
        "code": "sex",
        "status": "1",
        "remark": ""
    },
    {
        "id": 6,
        "name": "接口数据类型",
        "code": "api_data_type",
        "status": "1",
        "remark": ""
    },
    {
        "id": 7,
        "name": "后台公告类型",
        "code": "backend_notice_type",
        "status": "1",
        "remark": ""
    },
    {
        "id": 8,
        "name": "请求方式",
        "code": "request_mode",
        "status": "1",
        "remark": ""
    },
    {
        "id": 9,
        "name": "队列生产状态",
        "code": "queue_produce_status",
        "status": "1",
        "remark": ""
    },
    {
        "id": 10,
        "name": "队列消费状态",
        "code": "queue_consume_status",
        "status": "1",
        "remark": ""
    }
]

dictData = [
    {
        "id": 1,
        "type_id": 1,
        "label": "InnoDB",
        "value": "InnoDB",
        "code": "table_engine",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 2,
        "type_id": 1,
        "label": "MyISAM",
        "value": "MyISAM",
        "code": "table_engine",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 3,
        "type_id": 2,
        "label": "本地存储",
        "value": "1",
        "code": "upload_mode",
        "sort": 99,
        "status": "1",
        "remark": ""
    },
    {
        "id": 4,
        "type_id": 2,
        "label": "阿里云OSS",
        "value": "2",
        "code": "upload_mode",
        "sort": 98,
        "status": "1",
        "remark": ""
    },
    {
        "id": 5,
        "type_id": 2,
        "label": "七牛云",
        "value": "3",
        "code": "upload_mode",
        "sort": 97,
        "status": "1",
        "remark": ""
    },
    {
        "id": 6,
        "type_id": 2,
        "label": "腾讯云COS",
        "value": "4",
        "code": "upload_mode",
        "sort": 96,
        "status": "1",
        "remark": ""
    },
    {
        "id": 7,
        "type_id": 3,
        "label": "正常",
        "value": "1",
        "code": "data_status",
        "sort": 0,
        "status": "1",
        "remark": "0为正常"
    },
    {
        "id": 8,
        "type_id": 3,
        "label": "停用",
        "value": "2",
        "code": "data_status",
        "sort": 0,
        "status": "1",
        "remark": "1为停用"
    },
    {
        "id": 9,
        "type_id": 4,
        "label": "统计页面",
        "value": "statistics",
        "code": "dashboard",
        "sort": 0,
        "status": "1",
        "remark": "管理员用"
    },
    {
        "id": 10,
        "type_id": 4,
        "label": "工作台",
        "value": "work",
        "code": "dashboard",
        "sort": 0,
        "status": "1",
        "remark": "员工使用"
    },
    {
        "id": 11,
        "type_id": 5,
        "label": "男",
        "value": "1",
        "code": "sex",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 12,
        "type_id": 5,
        "label": "女",
        "value": "2",
        "code": "sex",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 13,
        "type_id": 5,
        "label": "未知",
        "value": "3",
        "code": "sex",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 14,
        "type_id": 6,
        "label": "String",
        "value": "1",
        "code": "api_data_type",
        "sort": 7,
        "status": "1",
        "remark": ""
    },
    {
        "id": 15,
        "type_id": 6,
        "label": "Integer",
        "value": "2",
        "code": "api_data_type",
        "sort": 6,
        "status": "1",
        "remark": ""
    },
    {
        "id": 16,
        "type_id": 6,
        "label": "Array",
        "value": "3",
        "code": "api_data_type",
        "sort": 5,
        "status": "1",
        "remark": ""
    },
    {
        "id": 17,
        "type_id": 6,
        "label": "Float",
        "value": "4",
        "code": "api_data_type",
        "sort": 4,
        "status": "1",
        "remark": ""
    },
    {
        "id": 18,
        "type_id": 6,
        "label": "Boolean",
        "value": "5",
        "code": "api_data_type",
        "sort": 3,
        "status": "1",
        "remark": ""
    },
    {
        "id": 19,
        "type_id": 6,
        "label": "Enum",
        "value": "6",
        "code": "api_data_type",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 20,
        "type_id": 6,
        "label": "Object",
        "value": "7",
        "code": "api_data_type",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 21,
        "type_id": 6,
        "label": "File",
        "value": "8",
        "code": "api_data_type",
        "sort": 0,
        "status": "1",
        "remark": ""
    },
    {
        "id": 22,
        "type_id": 7,
        "label": "通知",
        "value": "1",
        "code": "backend_notice_type",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 23,
        "type_id": 7,
        "label": "公告",
        "value": "2",
        "code": "backend_notice_type",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 24,
        "type_id": 8,
        "label": "所有",
        "value": "A",
        "code": "request_mode",
        "sort": 5,
        "status": "1",
        "remark": ""
    },
    {
        "id": 25,
        "type_id": 8,
        "label": "GET",
        "value": "G",
        "code": "request_mode",
        "sort": 4,
        "status": "1",
        "remark": ""
    },
    {
        "id": 26,
        "type_id": 8,
        "label": "POST",
        "value": "P",
        "code": "request_mode",
        "sort": 3,
        "status": "1",
        "remark": ""
    },
    {
        "id": 27,
        "type_id": 8,
        "label": "PUT",
        "value": "U",
        "code": "request_mode",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 28,
        "type_id": 8,
        "label": "DELETE",
        "value": "D",
        "code": "request_mode",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 29,
        "type_id": 9,
        "label": "未生产",
        "value": "1",
        "code": "queue_produce_status",
        "sort": 5,
        "status": "1",
        "remark": ""
    },
    {
        "id": 30,
        "type_id": 9,
        "label": "生产中",
        "value": "2",
        "code": "queue_produce_status",
        "sort": 4,
        "status": "1",
        "remark": ""
    },
    {
        "id": 31,
        "type_id": 9,
        "label": "生产成功",
        "value": "3",
        "code": "queue_produce_status",
        "sort": 3,
        "status": "1",
        "remark": ""
    },
    {
        "id": 32,
        "type_id": 9,
        "label": "生产失败",
        "value": "4",
        "code": "queue_produce_status",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 33,
        "type_id": 9,
        "label": "生产重复",
        "value": "5",
        "code": "queue_produce_status",
        "sort": 1,
        "status": "1",
        "remark": ""
    },
    {
        "id": 34,
        "type_id": 10,
        "label": "未消费",
        "value": "1",
        "code": "queue_consume_status",
        "sort": 5,
        "status": "1",
        "remark": ""
    },
    {
        "id": 35,
        "type_id": 10,
        "label": "消费中",
        "value": "2",
        "code": "queue_consume_status",
        "sort": 4,
        "status": "1",
        "remark": ""
    },
    {
        "id": 36,
        "type_id": 10,
        "label": "消费成功",
        "value": "3",
        "code": "queue_consume_status",
        "sort": 3,
        "status": "1",
        "remark": ""
    },
    {
        "id": 37,
        "type_id": 10,
        "label": "消费失败",
        "value": "4",
        "code": "queue_consume_status",
        "sort": 2,
        "status": "1",
        "remark": ""
    },
    {
        "id": 38,
        "type_id": 10,
        "label": "消费重复",
        "value": "5",
        "code": "queue_consume_status",
        "sort": 1,
        "status": "1",
        "remark": ""
    }
]

menuRelationData = [
    {
        "id": 1,
        "menu_id": 1000,
        "role_id": 1
    },
    {
        "id": 2,
        "menu_id": 1100,
        "role_id": 1
    },
    {
        "id": 3,
        "menu_id": 1101,
        "role_id": 1
    },
    {
        "id": 4,
        "menu_id": 1102,
        "role_id": 1
    },
    {
        "id": 5,
        "menu_id": 1103,
        "role_id": 1
    },
    {
        "id": 6,
        "menu_id": 1104,
        "role_id": 1
    },
    {
        "id": 7,
        "menu_id": 1105,
        "role_id": 1
    },
    {
        "id": 8,
        "menu_id": 1107,
        "role_id": 1
    },
    {
        "id": 9,
        "menu_id": 1108,
        "role_id": 1
    },
    {
        "id": 10,
        "menu_id": 1109,
        "role_id": 1
    },
    {
        "id": 11,
        "menu_id": 1110,
        "role_id": 1
    },
    {
        "id": 12,
        "menu_id": 1111,
        "role_id": 1
    },
    {
        "id": 13,
        "menu_id": 1112,
        "role_id": 1
    },
    {
        "id": 14,
        "menu_id": 1113,
        "role_id": 1
    },
    {
        "id": 15,
        "menu_id": 1114,
        "role_id": 1
    },
    {
        "id": 16,
        "menu_id": 1200,
        "role_id": 1
    },
    {
        "id": 17,
        "menu_id": 1201,
        "role_id": 1
    },
    {
        "id": 18,
        "menu_id": 1202,
        "role_id": 1
    },
    {
        "id": 19,
        "menu_id": 1203,
        "role_id": 1
    },
    {
        "id": 20,
        "menu_id": 1204,
        "role_id": 1
    },
    {
        "id": 21,
        "menu_id": 1205,
        "role_id": 1
    },
    {
        "id": 22,
        "menu_id": 1206,
        "role_id": 1
    },
    {
        "id": 23,
        "menu_id": 1207,
        "role_id": 1
    },
    {
        "id": 24,
        "menu_id": 1208,
        "role_id": 1
    },
    {
        "id": 25,
        "menu_id": 1209,
        "role_id": 1
    },
    {
        "id": 26,
        "menu_id": 1210,
        "role_id": 1
    },
    {
        "id": 27,
        "menu_id": 1300,
        "role_id": 1
    },
    {
        "id": 28,
        "menu_id": 1301,
        "role_id": 1
    },
    {
        "id": 29,
        "menu_id": 1302,
        "role_id": 1
    },
    {
        "id": 30,
        "menu_id": 1303,
        "role_id": 1
    },
    {
        "id": 31,
        "menu_id": 1304,
        "role_id": 1
    },
    {
        "id": 32,
        "menu_id": 1305,
        "role_id": 1
    },
    {
        "id": 33,
        "menu_id": 1306,
        "role_id": 1
    },
    {
        "id": 34,
        "menu_id": 1307,
        "role_id": 1
    },
    {
        "id": 35,
        "menu_id": 1308,
        "role_id": 1
    },
    {
        "id": 36,
        "menu_id": 1309,
        "role_id": 1
    },
    {
        "id": 37,
        "menu_id": 1310,
        "role_id": 1
    },
    {
        "id": 38,
        "menu_id": 1311,
        "role_id": 1
    },
    {
        "id": 39,
        "menu_id": 1400,
        "role_id": 1
    },
    {
        "id": 40,
        "menu_id": 1401,
        "role_id": 1
    },
    {
        "id": 41,
        "menu_id": 1402,
        "role_id": 1
    },
    {
        "id": 42,
        "menu_id": 1403,
        "role_id": 1
    },
    {
        "id": 43,
        "menu_id": 1404,
        "role_id": 1
    },
    {
        "id": 44,
        "menu_id": 1405,
        "role_id": 1
    },
    {
        "id": 45,
        "menu_id": 1406,
        "role_id": 1
    },
    {
        "id": 46,
        "menu_id": 1407,
        "role_id": 1
    },
    {
        "id": 47,
        "menu_id": 1408,
        "role_id": 1
    },
    {
        "id": 48,
        "menu_id": 1409,
        "role_id": 1
    },
    {
        "id": 49,
        "menu_id": 1410,
        "role_id": 1
    },
    {
        "id": 50,
        "menu_id": 1411,
        "role_id": 1
    },
    {
        "id": 51,
        "menu_id": 1412,
        "role_id": 1
    },
    {
        "id": 52,
        "menu_id": 1413,
        "role_id": 1
    },
    {
        "id": 53,
        "menu_id": 1500,
        "role_id": 1
    },
    {
        "id": 54,
        "menu_id": 1501,
        "role_id": 1
    },
    {
        "id": 55,
        "menu_id": 1502,
        "role_id": 1
    },
    {
        "id": 56,
        "menu_id": 1503,
        "role_id": 1
    },
    {
        "id": 57,
        "menu_id": 1504,
        "role_id": 1
    },
    {
        "id": 58,
        "menu_id": 1505,
        "role_id": 1
    },
    {
        "id": 59,
        "menu_id": 1506,
        "role_id": 1
    },
    {
        "id": 60,
        "menu_id": 1507,
        "role_id": 1
    },
    {
        "id": 61,
        "menu_id": 1508,
        "role_id": 1
    },
    {
        "id": 62,
        "menu_id": 1509,
        "role_id": 1
    },
    {
        "id": 63,
        "menu_id": 1510,
        "role_id": 1
    },
    {
        "id": 64,
        "menu_id": 1511,
        "role_id": 1
    },
    {
        "id": 65,
        "menu_id": 2000,
        "role_id": 1
    },
    {
        "id": 66,
        "menu_id": 2100,
        "role_id": 1
    },
    {
        "id": 67,
        "menu_id": 2101,
        "role_id": 1
    },
    {
        "id": 68,
        "menu_id": 2102,
        "role_id": 1
    },
    {
        "id": 69,
        "menu_id": 2103,
        "role_id": 1
    },
    {
        "id": 70,
        "menu_id": 2104,
        "role_id": 1
    },
    {
        "id": 71,
        "menu_id": 2105,
        "role_id": 1
    },
    {
        "id": 72,
        "menu_id": 2106,
        "role_id": 1
    },
    {
        "id": 73,
        "menu_id": 2107,
        "role_id": 1
    },
    {
        "id": 74,
        "menu_id": 2108,
        "role_id": 1
    },
    {
        "id": 75,
        "menu_id": 2109,
        "role_id": 1
    },
    {
        "id": 76,
        "menu_id": 2110,
        "role_id": 1
    },
    {
        "id": 77,
        "menu_id": 2111,
        "role_id": 1
    },
    {
        "id": 78,
        "menu_id": 2112,
        "role_id": 1
    },
    {
        "id": 79,
        "menu_id": 2200,
        "role_id": 1
    },
    {
        "id": 80,
        "menu_id": 2201,
        "role_id": 1
    },
    {
        "id": 81,
        "menu_id": 2202,
        "role_id": 1
    },
    {
        "id": 82,
        "menu_id": 2203,
        "role_id": 1
    },
    {
        "id": 83,
        "menu_id": 2204,
        "role_id": 1
    },
    {
        "id": 84,
        "menu_id": 2205,
        "role_id": 1
    },
    {
        "id": 85,
        "menu_id": 2206,
        "role_id": 1
    },
    {
        "id": 86,
        "menu_id": 2207,
        "role_id": 1
    },
    {
        "id": 87,
        "menu_id": 2208,
        "role_id": 1
    },
    {
        "id": 88,
        "menu_id": 2209,
        "role_id": 1
    },
    {
        "id": 89,
        "menu_id": 2210,
        "role_id": 1
    },
    {
        "id": 90,
        "menu_id": 2300,
        "role_id": 1
    },
    {
        "id": 91,
        "menu_id": 2301,
        "role_id": 1
    },
    {
        "id": 92,
        "menu_id": 2302,
        "role_id": 1
    },
    {
        "id": 93,
        "menu_id": 2303,
        "role_id": 1
    },
    {
        "id": 94,
        "menu_id": 2304,
        "role_id": 1
    },
    {
        "id": 95,
        "menu_id": 2500,
        "role_id": 1
    },
    {
        "id": 96,
        "menu_id": 2510,
        "role_id": 1
    },
    {
        "id": 97,
        "menu_id": 2530,
        "role_id": 1
    },
    {
        "id": 98,
        "menu_id": 2600,
        "role_id": 1
    },
    {
        "id": 99,
        "menu_id": 2610,
        "role_id": 1
    },
    {
        "id": 100,
        "menu_id": 2630,
        "role_id": 1
    },
    {
        "id": 101,
        "menu_id": 2700,
        "role_id": 1
    },
    {
        "id": 102,
        "menu_id": 2701,
        "role_id": 1
    },
    {
        "id": 103,
        "menu_id": 2702,
        "role_id": 1
    },
    {
        "id": 104,
        "menu_id": 2703,
        "role_id": 1
    },
    {
        "id": 105,
        "menu_id": 2704,
        "role_id": 1
    },
    {
        "id": 106,
        "menu_id": 2705,
        "role_id": 1
    },
    {
        "id": 107,
        "menu_id": 2706,
        "role_id": 1
    },
    {
        "id": 108,
        "menu_id": 2707,
        "role_id": 1
    },
    {
        "id": 109,
        "menu_id": 2708,
        "role_id": 1
    },
    {
        "id": 110,
        "menu_id": 2709,
        "role_id": 1
    },
    {
        "id": 111,
        "menu_id": 2710,
        "role_id": 1
    },
    {
        "id": 112,
        "menu_id": 3000,
        "role_id": 1
    },
    {
        "id": 113,
        "menu_id": 3100,
        "role_id": 1
    },
    {
        "id": 114,
        "menu_id": 3101,
        "role_id": 1
    },
    {
        "id": 115,
        "menu_id": 3200,
        "role_id": 1
    },
    {
        "id": 116,
        "menu_id": 3300,
        "role_id": 1
    },
    {
        "id": 117,
        "menu_id": 3400,
        "role_id": 1
    },
    {
        "id": 118,
        "menu_id": 3500,
        "role_id": 1
    },
    {
        "id": 119,
        "menu_id": 3600,
        "role_id": 1
    },
    {
        "id": 120,
        "menu_id": 3700,
        "role_id": 1
    },
    {
        "id": 121,
        "menu_id": 3701,
        "role_id": 1
    },
    {
        "id": 122,
        "menu_id": 3702,
        "role_id": 1
    },
    {
        "id": 123,
        "menu_id": 3703,
        "role_id": 1
    },
    {
        "id": 124,
        "menu_id": 3800,
        "role_id": 1
    },
    {
        "id": 125,
        "menu_id": 3850,
        "role_id": 1
    },
    {
        "id": 126,
        "menu_id": 4000,
        "role_id": 1
    },
    {
        "id": 127,
        "menu_id": 4100,
        "role_id": 1
    },
    {
        "id": 128,
        "menu_id": 4101,
        "role_id": 1
    },
    {
        "id": 129,
        "menu_id": 4102,
        "role_id": 1
    },
    {
        "id": 130,
        "menu_id": 4103,
        "role_id": 1
    },
    {
        "id": 131,
        "menu_id": 4104,
        "role_id": 1
    },
    {
        "id": 132,
        "menu_id": 4105,
        "role_id": 1
    },
    {
        "id": 133,
        "menu_id": 4200,
        "role_id": 1
    },
    {
        "id": 134,
        "menu_id": 4201,
        "role_id": 1
    },
    {
        "id": 135,
        "menu_id": 4202,
        "role_id": 1
    },
    {
        "id": 136,
        "menu_id": 4203,
        "role_id": 1
    },
    {
        "id": 137,
        "menu_id": 4204,
        "role_id": 1
    },
    {
        "id": 138,
        "menu_id": 4205,
        "role_id": 1
    },
    {
        "id": 139,
        "menu_id": 4206,
        "role_id": 1
    },
    {
        "id": 140,
        "menu_id": 4300,
        "role_id": 1
    },
    {
        "id": 141,
        "menu_id": 4301,
        "role_id": 1
    },
    {
        "id": 142,
        "menu_id": 4400,
        "role_id": 1
    },
    {
        "id": 143,
        "menu_id": 4401,
        "role_id": 1
    },
    {
        "id": 144,
        "menu_id": 4402,
        "role_id": 1
    },
    {
        "id": 145,
        "menu_id": 4403,
        "role_id": 1
    },
    {
        "id": 146,
        "menu_id": 4404,
        "role_id": 1
    },
    {
        "id": 147,
        "menu_id": 4405,
        "role_id": 1
    },
    {
        "id": 148,
        "menu_id": 4406,
        "role_id": 1
    },
    {
        "id": 149,
        "menu_id": 4407,
        "role_id": 1
    },
    {
        "id": 150,
        "menu_id": 4408,
        "role_id": 1
    },
    {
        "id": 151,
        "menu_id": 4409,
        "role_id": 1
    },
    {
        "id": 152,
        "menu_id": 4500,
        "role_id": 1
    },
    {
        "id": 153,
        "menu_id": 4501,
        "role_id": 1
    },
    {
        "id": 154,
        "menu_id": 4502,
        "role_id": 1
    },
    {
        "id": 155,
        "menu_id": 4503,
        "role_id": 1
    },
    {
        "id": 156,
        "menu_id": 4504,
        "role_id": 1
    },
    {
        "id": 157,
        "menu_id": 4505,
        "role_id": 1
    },
    {
        "id": 158,
        "menu_id": 4506,
        "role_id": 1
    },
    {
        "id": 159,
        "menu_id": 4507,
        "role_id": 1
    },
    {
        "id": 160,
        "menu_id": 4600,
        "role_id": 1
    },
    {
        "id": 161,
        "menu_id": 4601,
        "role_id": 1
    },
]

routerData = [
    {
        "id": 1000,
        "name": "permission",
        "path": "/permission",
        "hidden": "0",
        "parent_id": "0",
        "icon": "el-icon-stamp",
        "redirect": "",
        "title": "权限管理",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1100,
        "name": "system:user",
        "path": "/user",
        "hidden": "0",
        "parent_id": 1000,
        "icon": "ma-icon-user",
        "redirect": "",
        "title": "用户管理",
        "type": "M",
        "component": "system/user/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1101,
        "name": "system:user:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1102,
        "name": "system:user:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户回收站列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1103,
        "name": "system:user:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1104,
        "name": "system:user:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1105,
        "name": "system:user:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1107,
        "name": "system:user:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1108,
        "name": "system:user:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1109,
        "name": "system:user:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1110,
        "name": "system:user:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1111,
        "name": "system:user:changeStatus",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户状态改变",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1112,
        "name": "system:user:initUserPassword",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "用户初始化密码",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1113,
        "name": "system:user:cache",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "更新用户缓存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1114,
        "name": "system:user:homePage",
        "path": "/",
        "hidden": "0",
        "parent_id": 1100,
        "icon": "",
        "redirect": "",
        "title": "设置用户首页",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1200,
        "name": "system:menu",
        "path": "/menu",
        "hidden": "0",
        "parent_id": 1000,
        "icon": "el-icon-message-box",
        "redirect": "",
        "title": "菜单管理",
        "type": "M",
        "component": "system/menu/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1201,
        "name": "system:menu:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1202,
        "name": "system:menu:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1203,
        "name": "system:menu:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1204,
        "name": "system:menu:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1205,
        "name": "system:menu:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1206,
        "name": "system:menu:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1207,
        "name": "system:menu:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1208,
        "name": "system:menu:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1209,
        "name": "system:menu:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1210,
        "name": "system:menu:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 1200,
        "icon": "",
        "redirect": "",
        "title": "菜单导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1300,
        "name": "system:dept",
        "path": "/dept",
        "hidden": "0",
        "parent_id": 1000,
        "icon": "ma-icon-rely",
        "redirect": "",
        "title": "部门管理",
        "type": "M",
        "component": "system/dept/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1301,
        "name": "system:dept:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1302,
        "name": "system:dept:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1303,
        "name": "system:dept:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1304,
        "name": "system:dept:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1305,
        "name": "system:dept:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1306,
        "name": "system:dept:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1307,
        "name": "system:dept:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1308,
        "name": "system:dept:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1309,
        "name": "system:dept:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1310,
        "name": "system:dept:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1311,
        "name": "system:dept:changeStatus",
        "path": "/",
        "hidden": "0",
        "parent_id": 1300,
        "icon": "",
        "redirect": "",
        "title": "部门状态改变",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1400,
        "name": "system:role",
        "path": "/role",
        "hidden": "0",
        "parent_id": 1000,
        "icon": "ma-icon-role",
        "redirect": "",
        "title": "角色管理",
        "type": "M",
        "component": "system/role/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1401,
        "name": "system:role:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1402,
        "name": "system:role:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1403,
        "name": "system:role:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1404,
        "name": "system:role:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1405,
        "name": "system:role:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1406,
        "name": "system:role:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1407,
        "name": "system:role:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1408,
        "name": "system:role:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1409,
        "name": "system:role:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1410,
        "name": "system:role:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1411,
        "name": "system:role:changeStatus",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "角色状态改变",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1412,
        "name": "system:role:menuPermission",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "更新菜单权限",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1413,
        "name": "system:role:dataPermission",
        "path": "/",
        "hidden": "0",
        "parent_id": 1400,
        "icon": "",
        "redirect": "",
        "title": "更新数据权限",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1500,
        "name": "system:post",
        "path": "/post",
        "hidden": "0",
        "parent_id": 1000,
        "icon": "el-icon-coffee-cup",
        "redirect": "",
        "title": "岗位管理",
        "type": "M",
        "component": "system/post/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1501,
        "name": "system:post:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1502,
        "name": "system:post:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1503,
        "name": "system:post:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1504,
        "name": "system:post:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1505,
        "name": "system:post:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1506,
        "name": "system:post:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1507,
        "name": "system:post:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1508,
        "name": "system:post:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1509,
        "name": "system:post:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1510,
        "name": "system:post:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 1511,
        "name": "system:post:changeStatus",
        "path": "/",
        "hidden": "0",
        "parent_id": 1500,
        "icon": "",
        "redirect": "",
        "title": "岗位状态改变",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2000,
        "name": "dataCenter",
        "path": "/dataCenter",
        "hidden": "0",
        "parent_id": "0",
        "icon": "el-icon-histogram",
        "redirect": "",
        "title": "数据中心",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2100,
        "name": "system:dict",
        "path": "/dict",
        "hidden": "0",
        "parent_id": 2000,
        "icon": "ma-icon-dict",
        "redirect": "",
        "title": "数据字典",
        "type": "M",
        "component": "system/dict/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2101,
        "name": "system:dataDict:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2102,
        "name": "system:dataDict:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2103,
        "name": "system:dataDict:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2104,
        "name": "system:dataDict:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2105,
        "name": "system:dataDict:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2106,
        "name": "system:dataDict:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2107,
        "name": "system:dataDict:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2108,
        "name": "system:dataDict:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2109,
        "name": "system:dataDict:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2110,
        "name": "system:dataDict:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "数据字典导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2111,
        "name": "system:dataDict:clearCache",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "清除字典缓存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2112,
        "name": "system:dataDict:changeStatus",
        "path": "/",
        "hidden": "0",
        "parent_id": 2100,
        "icon": "",
        "redirect": "",
        "title": "字典状态改变",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2200,
        "name": "system:dictType",
        "path": "/dictType",
        "hidden": "1",
        "parent_id": 2000,
        "icon": "",
        "redirect": "",
        "title": "字典类型",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2201,
        "name": "system:dictType:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2202,
        "name": "system:dictType:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2203,
        "name": "system:dictType:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2204,
        "name": "system:dictType:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2205,
        "name": "system:dictType:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2206,
        "name": "system:dictType:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2207,
        "name": "system:dictType:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2208,
        "name": "system:dictType:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2209,
        "name": "system:dictType:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2210,
        "name": "system:dictType:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 2200,
        "icon": "",
        "redirect": "",
        "title": "字典类型导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2300,
        "name": "system:attachment",
        "path": "/attachment",
        "hidden": "0",
        "parent_id": 2000,
        "icon": "ma-icon-attach",
        "redirect": "",
        "title": "附件管理",
        "type": "M",
        "component": "system/attachment/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2301,
        "name": "system:attachment:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2300,
        "icon": "",
        "redirect": "",
        "title": "附件删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2302,
        "name": "system:attachment:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 2300,
        "icon": "",
        "redirect": "",
        "title": "附件列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2303,
        "name": "system:attachment:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 2300,
        "icon": "",
        "redirect": "",
        "title": "附件回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2304,
        "name": "system:attachment:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2300,
        "icon": "",
        "redirect": "",
        "title": "附件真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2500,
        "name": "apps",
        "path": "/apps",
        "hidden": "0",
        "parent_id": 2000,
        "icon": "el-icon-goods",
        "redirect": "",
        "title": "应用中心",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2510,
        "name": "system:appGroup",
        "path": "/appGroup",
        "hidden": "0",
        "parent_id": 2500,
        "icon": "",
        "redirect": "",
        "title": "应用分组",
        "type": "M",
        "component": "system/appGroup/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2530,
        "name": "system:app",
        "path": "/app",
        "hidden": "0",
        "parent_id": 2500,
        "icon": "",
        "redirect": "",
        "title": "应用管理",
        "type": "M",
        "component": "system/app/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2600,
        "name": "apis",
        "path": "/apis",
        "hidden": "0",
        "parent_id": 2000,
        "icon": "el-icon-set-up",
        "redirect": "",
        "title": "应用接口",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2610,
        "name": "system:apiGroup",
        "path": "/apiGroup",
        "hidden": "0",
        "parent_id": 2600,
        "icon": "",
        "redirect": "",
        "title": "接口分组",
        "type": "M",
        "component": "system/apiGroup/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2630,
        "name": "system:api",
        "path": "/api",
        "hidden": "0",
        "parent_id": 2600,
        "icon": "",
        "redirect": "",
        "title": "接口管理",
        "type": "M",
        "component": "system/api/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2700,
        "name": "system:notice",
        "path": "/notice",
        "hidden": "0",
        "parent_id": 2000,
        "icon": "el-icon-bell",
        "redirect": "",
        "title": "系统公告",
        "type": "M",
        "component": "system/notice/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2701,
        "name": "system:notice:index",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告列表",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2702,
        "name": "system:notice:recycle",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告回收站",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2703,
        "name": "system:notice:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告保存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2704,
        "name": "system:notice:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告更新",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2705,
        "name": "system:notice:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2706,
        "name": "system:notice:read",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告读取",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2707,
        "name": "system:notice:recovery",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告恢复",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2708,
        "name": "system:notice:realDelete",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告真实删除",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2709,
        "name": "system:notice:import",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告导入",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 2710,
        "name": "system:notice:export",
        "path": "/",
        "hidden": "0",
        "parent_id": 2700,
        "icon": "",
        "redirect": "",
        "title": "系统公告导出",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3000,
        "name": "monitor",
        "path": "/monitor",
        "hidden": "0",
        "parent_id": "0",
        "icon": "el-icon-trend-charts",
        "redirect": "",
        "title": "系统监控",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3200,
        "name": "system:monitor:server",
        "path": "/server",
        "hidden": "0",
        "parent_id": 3000,
        "icon": "el-icon-umbrella",
        "redirect": "",
        "title": "服务监控",
        "type": "M",
        "component": "system/monitor/server/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3300,
        "name": "logs",
        "path": "/logs",
        "hidden": "0",
        "parent_id": 3000,
        "icon": "el-icon-calendar",
        "redirect": "",
        "title": "日志监控",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3400,
        "name": "system:loginLog",
        "path": "/loginLog",
        "hidden": "0",
        "parent_id": 3300,
        "icon": "el-icon-reading",
        "redirect": "",
        "title": "登录日志",
        "type": "M",
        "component": "system/loginLog/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3500,
        "name": "system:operLog",
        "path": "/operLog",
        "hidden": "0",
        "parent_id": 3300,
        "icon": "el-icon-document",
        "redirect": "",
        "title": "操作日志",
        "type": "M",
        "component": "system/operLog/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3600,
        "name": "system:onlineUser",
        "path": "/onlineUser",
        "hidden": "0",
        "parent_id": 3000,
        "icon": "ma-icon-online",
        "redirect": "",
        "title": "在线用户",
        "type": "M",
        "component": "system/monitor/onlineUser/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3700,
        "name": "system:cache",
        "path": "/cache",
        "hidden": "0",
        "parent_id": 3000,
        "icon": "el-icon-cpu",
        "redirect": "",
        "title": "缓存监控",
        "type": "M",
        "component": "system/monitor/cache/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3701,
        "name": "system:cache:monitor",
        "path": "/",
        "hidden": "0",
        "parent_id": 3700,
        "icon": "",
        "redirect": "",
        "title": "获取Redis信息",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3702,
        "name": "system:cache:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 3700,
        "icon": "",
        "redirect": "",
        "title": "删除一个缓存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3703,
        "name": "system:cache:clear",
        "path": "/",
        "hidden": "0",
        "parent_id": 3700,
        "icon": "",
        "redirect": "",
        "title": "清空所有缓存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 3850,
        "name": "system:queueLog",
        "path": "/queueLog",
        "hidden": "0",
        "parent_id": 3300,
        "icon": "el-icon-guide",
        "redirect": "",
        "title": "队列日志",
        "type": "M",
        "component": "system/queueLog/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4000,
        "name": "devTools",
        "path": "/devTools",
        "hidden": "0",
        "parent_id": "0",
        "icon": "el-icon-menu",
        "redirect": "",
        "title": "开发工具",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4500,
        "name": "setting:config",
        "path": "/setting",
        "hidden": "1",
        "parent_id": "0",
        "icon": "",
        "redirect": "",
        "title": "系统设置",
        "type": "M",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4501,
        "name": "setting:config:getSystemConfig",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "获取系统组配置",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4502,
        "name": "setting:config:getExtendConfig",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "获取扩展组配置",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4503,
        "name": "setting:config:saveSystemConfig",
        "path": "/",
        "hidden": "0",
        "parent_id": 3600,
        "icon": "",
        "redirect": "",
        "title": "保存系统组配置",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4504,
        "name": "setting:config:save",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "新增配置 ",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4505,
        "name": "setting:config:update",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "更新配置",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4506,
        "name": "setting:config:delete",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "删除配置",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4507,
        "name": "setting:config:clearCache",
        "path": "/",
        "hidden": "0",
        "parent_id": 4500,
        "icon": "",
        "redirect": "",
        "title": "清除配置缓存",
        "type": "B",
        "component": "",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4600,
        "name": "systemInterface",
        "path": "/systemInterface",
        "hidden": "0",
        "parent_id": 4000,
        "icon": "el-icon-document",
        "redirect": "",
        "title": "系统接口",
        "type": "M",
        "component": "setting/systemInterface/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    },
    {
        "id": 4601,
        "name": "formDesigner",
        "path": "/formDesigner",
        "hidden": "0",
        "parent_id": 4000,
        "icon": "el-icon-takeaway-box",
        "redirect": "",
        "title": "表单设计器",
        "type": "M",
        "component": "setting/formDesigner/index",
        "status": "1",
        "sort": "0",
        "level": "0"
    }
]