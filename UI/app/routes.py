from flask import Blueprint
import controller as c

main = Blueprint('main',__name__, url_prefix="/")

main.route("/",                                 methods=['GET', 'POST'])    (c.login)
main.route("/logout",                           methods=['GET'])            (c.logout)
main.route("/index",                            methods=['GET'])            (c.index)
main.route("/policy",                           methods=['GET', 'POST'])    (c.policy)