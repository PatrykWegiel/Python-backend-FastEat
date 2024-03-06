from rest_framework.exceptions import APIException


class UserUnauthorized(APIException):
    status_code = 401
    default_detail = "User unauthorized"
    default_code = "user_unauthorized"
