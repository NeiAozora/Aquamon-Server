import inspect
from functools import wraps

class Route:
    def __init__(self, app):
        self.app = app
        self._route_map = {}

    def add(self, endpoint, controller, method=None, http_methods=None, alias=None):
        if method is None:
            if not callable(controller):
                raise ValueError("Expected a callable function when 'method' is not provided")
            view_func = controller
            name = controller.__name__
        else:
            if isinstance(controller, type):
                raw_attr = inspect.getattr_static(controller, method)
                if isinstance(raw_attr, staticmethod):
                    view_func = raw_attr.__func__
                else:
                    # Dynamic instance creation and cleanup
                    @wraps(getattr(controller, method))
                    def wrapped(*args, **kwargs):
                        instance = controller()
                        try:
                            return getattr(instance, method)(*args, **kwargs)
                        finally:
                            del instance
                    view_func = wrapped
                name = controller.__name__
            else:
                view_func = getattr(controller, method)
                name = controller.__class__.__name__

        endpoint_name = alias or f"{name}_{method}" if method else name
        self._route_map[endpoint_name] = view_func

        self.app.add_url_rule(
            endpoint,
            endpoint_name,
            view_func,
            methods=http_methods
        )

    def get_route(self, alias):
        return self._route_map.get(alias)

    def get(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["GET"], alias)

    def post(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["POST"], alias)

    def put(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["PUT"], alias)

    def delete(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["DELETE"], alias)

    def patch(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["PATCH"], alias)

    def options(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["OPTIONS"], alias)

    def head(self, endpoint, controller, method=None, alias=None):
        self.add(endpoint, controller, method, ["HEAD"], alias)
