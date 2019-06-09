from rest_framework.exceptions import APIException


class CountryDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested country does not exist.'


class CountyDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested county does not exist.'


class ConstituencyDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested constituency does not exist.'


class WardDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested ward does not exist.'