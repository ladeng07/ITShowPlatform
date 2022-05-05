def get_error_msg(code="20000"):
    error_set = {
        "20000": "成功",
        "50000": "意外错误",
        "50403": "Forbidden",
        "40000": "请求方法错误",
        "40001": "JSON解析错误",
        "45030": "信息不存在",
        "45032": "邮箱验证码过期",
        "44031": "邮箱验证码错误",
        "44032": "请先发送验证码",
        "43032": "该邮箱已存在",
        "43033": "该手机号码已存在",
        "42033": "手机号码不合规",
        "42034": "姓名过长",
        "42035": "说的太多啦",
        "42032": "邮箱过长",
        "44033": "请勿频繁发送验证码",
        "44036": "请输入正确格式的邮箱",

        "40002": "非法字符",
        "40003": "弹幕过长",
        "40004": "输入不能为空",
        "40005": "返回评论数为0",
        "40006": "",
    }
    return error_set.get(str(code))
