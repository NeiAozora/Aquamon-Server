class Route:
    def __init__(self, app):
        self.app = app  # Store the Flask app instance

    def add(self, endpoint, controller, method, http_methods):
        """
        General method to add a route with specified HTTP methods.
        """
        self.app.add_url_rule(
            endpoint,
            controller.__name__ + '_' + method,
            getattr(controller, method),
            methods=http_methods
        )

    def get(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["GET"])

    def post(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["POST"])

    def put(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["PUT"])

    def delete(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["DELETE"])

    def patch(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["PATCH"])

    def options(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["OPTIONS"])

    def head(self, endpoint, controller, method):
        self.add(endpoint, controller, method, ["HEAD"])
