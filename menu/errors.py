from rest_framework.exceptions import APIException


class VenueDoesntExits(APIException):
    status_code = 404
    default_detail = "Venue does not exist"
    default_code = "venue_doesnt_exits"


class MenuDoesntExits(APIException):
    status_code = 404
    default_detail = "Menu does not exist"
    default_code = "menu_doesnt_exits"


class MenuAlreadyExits(APIException):
    status_code = 400
    default_detail = "Menu already exists"
    default_code = "menu_already_exits"


class CategoryDoesntExits(APIException):
    status_code = 404
    default_detail = "Category does not exist"
    default_code = "category_doesnt_exits"


class ItemDoesntExits(APIException):
    status_code = 404
    default_detail = "Item does not exist"
    default_code = "item_doesnt_exits"


class AddonDoesntExits(APIException):
    status_code = 404
    default_detail = "Addon does not exist"
    default_code = "addon_doesnt_exits"
