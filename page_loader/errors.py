class AppInternalError(Exception):
    pass


class NetError(AppInternalError):
    pass


class SaveError(AppInternalError):
    pass
