from rest_framework.exceptions import APIException


class CartDoesntExist(APIException):
    status_code = 404
    default_detail = "Cart does not exist"
    default_code = "cart_doesnt_exist"


class CartItemDoesntExist(APIException):
    status_code = 404
    default_detail = "Cart item does not exist"
    default_code = "cart_item_doesnt_exist"


class CartAlreadyExists(APIException):
    status_code = 400
    default_detail = "Cart already exists"
    default_code = "cart_already_exists"


class CartItemAlreadyExists(APIException):
    status_code = 400
    default_detail = "Item already exists in cart"
    default_code = "cart_item_already_exists"


class WrongMenuItem(APIException):
    status_code = 400
    default_detail = "This item does not belong to this venue"
    default_code = "wrong_menu_item"


class WrongItemAddon(APIException):
    status_code = 400
    default_detail = "Wrong addon for this item"
    default_code = "wrong_item_addon"
