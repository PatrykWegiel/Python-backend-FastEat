from rest_framework.exceptions import APIException


class VenueDoesntExists(APIException):
    status = 404
    default_detail = "Venue doesn't exist"
    default_code = "venue_doesnt_exist"


class UserFavoriteVenueDoesntExist(APIException):
    status = 404
    default_detail = "Venue does not in favorites list"
    default_code = "user_favorite_venue_doesnt_exist"


class UserFavoriteVenueAlreadyExists(APIException):
    status = 404
    default_detail = "Venue is already in favorites list"
    default_code = "user_favorite_venue_doesnt_exist"


class RequiredImage(APIException):
    status = 404
    default_detail = "Image file is missing"
    default_code = "image_missing"
