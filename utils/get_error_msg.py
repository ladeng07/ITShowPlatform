def get_error_msg(code="20000"):
    error_set = {
        "20000": "成功",
        "50000": "意外错误",
        "50403": "Forbidden",
        "40000": "请求方法错误",
        "40001": "JSON解析错误",
    }
    return error_set.get(str(code))
