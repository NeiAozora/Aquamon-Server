from flask import render_template
from flask import Blueprint
from core.route import Route
from controllers.client.login_controller import LoginController;


def register_routes(app):
    
    route = Route(app)
    
    
    # client side
    route.post("/client/auth", LoginController, 'login')
    
    
