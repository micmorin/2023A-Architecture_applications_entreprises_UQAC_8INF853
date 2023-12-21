from flask import Blueprint
import controller as c

main = Blueprint('main',__name__, url_prefix="/")

main.route("/",                                         methods=['POST'])    (c.index)
main.route("/addPolicy",                                methods=['POST'])    (c.add_policy)
main.route("/removePolicy",                             methods=['POST'])    (c.delete_policy)
main.route("/updatePolicy",                             methods=['POST'])    (c.update_policy)
main.route("/getPolicies",                              methods=['GET'])     (c.get_policies)

