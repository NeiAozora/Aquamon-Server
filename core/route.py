import inspect
import types

class Route:
    def __init__(self, app):
        self.app = app

    def add(self, endpoint, controller, method=None, http_methods=None):
        if method is None:
            # Plain function
            if not callable(controller):
                raise ValueError("Expected a callable function when 'method' is not provided")
            view_func = controller
            endpoint_name = controller.__name__
        else:
            # Method from class or instance
            attr = getattr(controller, method)

            if isinstance(attr, staticmethod):
                # For staticmethods (from class only)
                view_func = attr.__func__
                name = controller.__name__ if isinstance(controller, type) else controller.__class__.__name__
            elif isinstance(controller, type):
                # It's a class, check if method is static
                raw_attr = inspect.getattr_static(controller, method)
                if isinstance(raw_attr, staticmethod):
                    view_func = raw_attr.__func__
                else:
                    instance = controller()
                    view_func = getattr(instance, method)
                name = controller.__name__
            else:
                # Already an instance
                view_func = getattr(controller, method)
                name = controller.__class__.__name__

            endpoint_name = f"{name}_{method}"

        self.app.add_url_rule(
            endpoint,
            endpoint_name,
            view_func,
            methods=http_methods
        )

    def get(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["GET"])

    def post(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["POST"])

    def put(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["PUT"])

    def delete(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["DELETE"])

    def patch(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["PATCH"])

    def options(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["OPTIONS"])

    def head(self, endpoint, controller, method=None):
        self.add(endpoint, controller, method, ["HEAD"])
