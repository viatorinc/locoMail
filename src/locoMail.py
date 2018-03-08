import asyncore

from flask import Flask
from flask import Response
from flask import render_template
from flask import make_response
import json
from mailDAO import MailDAO
from mailDTO import MailWrapper
from locoThread import ThreadedSMTP
from collections import OrderedDict
import re
import base64
import logging

mail_dao = MailDAO()

SMTP_PORT = 25
mail_server = ThreadedSMTP()
mail_server.start(SMTP_PORT)

app = Flask(__name__)
app.debug = True


def app_help():
    """
    Simple helper method to get a list of all available urls calls...
    :return:
    """
    import urllib
    output = []

    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            help = app.view_functions[rule.endpoint].__doc__
            if help:
                help = re.sub(".*return.*\n","",help).replace("\n",'<br/>')
                func_list[rule.rule] = help

    ordered = OrderedDict(func_list)

    return ordered


@app.route('/')
def all():
    return render_template("index.html", mails=mail_dao.get_all())


@app.route("/id/<id>")
def by_id(id):
    mail = mail_dao.get_by_id(int(id))
    return render_template("mail.html", mail=mail)

@app.route("/id/delete/<id>")
def delete_by_id(id):
    mail_dao.delete_by_id(int(id))
    return all()

@app.route("/files/<mail_id>/<file_name>")
def mail_file(mail_id, file_name):

    attachments = mail_dao.get_attachments(int(mail_id))
    attachment = attachments[file_name]
    binary = base64.b64decode(attachment)

    response = make_response(binary)
    response.headers["Content-Disposition"] = 'attachment; filename=%s' % file_name
    return response


"""
Api methods!
"""
@app.route("/api/")
def api_base():
    instructions = app_help()
    urls = sorted(instructions.keys())
    return render_template("api.html", urls=urls, help=instructions)


@app.route("/api/all")
def api_all():
    """
    Gets a list of all the emails.
    """
    all_mail = mail_dao.get_all()
    return _create_response(all_mail)


@app.route("/api/id/delete/<id>")
def api_delete_by_id(id):
    """
    Deletes the given mail id. Returns a list with the rest of mails
    """
    mail_dao.delete_by_id(int(id))
    return api_all()


@app.route("/api/id/<id>")
def api_by_id(id):
    """
    Gets the mail linked to this id
    """
    mail = mail_dao.get_by_id(int(id))
    return _create_response([mail])


@app.route("/api/files/<mail_id>")
def api_mail_files(mail_id):
    """
    Gets the the attachments for this mail id. Attachments are encoded as base64 strings
    """
    attachments = mail_dao.get_attachments(int(mail_id))
    return Response(response=json.dumps(attachments),
                    status=200,
                    mimetype='application/json')


@app.route("/api/files/<mail_id>/<file_name>")
def api_mail_file(mail_id, file_name):
    """
    Gets a single attachment for the given email. Attachment is encoded in base64
    """
    attachments = mail_dao.get_attachments(int(mail_id))
    return Response(response=json.dumps(attachments[file_name]),
                    status=200,
                    mimetype='application/json')


@app.route("/api/from/<from_address>")
def api_by_from(from_address):
    """
    Gets all the mails from a given mail address
    """
    mail = mail_dao.get_by_from_address(from_address)
    return _create_response(mail)


@app.route("/api/to/<to_address>")
def api_by_to(to_address):
    """
    Gets all the mails sent to the given mail address
    """
    mail = mail_dao.get_by_to_address(to_address)
    return _create_response(mail)


def _create_response(raws: [MailWrapper], status=200, mimetpe='application/json') :
    """
      helper function to create response
    :param details:response details
    :param status: http status
    :return Response:
    """
    results = []
    for raw in raws:
        results.append(raw.as_dict())


    return Response(response=json.dumps(results),
                    status=status,
                    mimetype=mimetpe)



if __name__ == '__main__':

    app.run()
