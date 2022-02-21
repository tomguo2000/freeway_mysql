from flask import request

def requestID4response(f):
    def decorated(*args, **kwargs):

        # 执行被装饰的函数自身
        result = f(*args, **kwargs)

        # 添加原始请求的headers中的 request-Id 到被装饰函数的response中
        requestID = request.headers.get('request-Id')       # 原始请求不含request-Id，就给安排个None
        result += tuple([{'request-Id': requestID}])

        return result
    return decorated
