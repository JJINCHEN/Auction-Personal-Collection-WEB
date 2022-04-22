# -*- coding:utf-8 -*-

from django.http import JsonResponse


class HttpCode(object):
    success = 0
    error = 1


def result(code=HttpCode.success, message='', data=None, kwargs=None, count=None):
    json_dict = {'data': data, 'code': code, 'message': message, 'count':count}
    print(json_dict)
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict, json_dumps_params={'ensure_ascii': False})


def success(data=None):
    return result(code=HttpCode.success, message='OK', data=data)


def success_by_count(data=None, count=""):
    return result(code=HttpCode.success, message='OK', data=data, count=count)


def error(message='', data=None):
    return result(code=HttpCode.error, message=message, data=data)