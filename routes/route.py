from flask import render_template
from flask import Blueprint
from flask import Response
from core.route import Route
from core.logger import Logger
from controllers.client.login_controller import LoginController;
from controllers.iot.kolam_controller import KolamController as IOTKolamController;
from controllers.client.register_controller import RegisterController;



def test():
    Logger.get_logger().debug("Ping!")
    
    res = Response()
    res.status = 200
    return res




def register_routes(app):
    
    route = Route(app)
    
    route.get("/api/test", test)
    
    # client side
    route.post("/api/client/auth", LoginController, 'login')
    route.post("/api/client/register", RegisterController, "register")
    
    
    # IOT side
    
    route.post("/api/iot/send-status", IOTKolamController, "update_status"); 
    
    
