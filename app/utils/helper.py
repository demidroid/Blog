import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.text import MIMEText


def request_loads(request, schema) -> tuple:
    args = request.args or dict()
    s = schema()
    if request.json:
        args.update(request.json)
    data, error = s.load(args)
    return data, error


def data_dumps(data, schema) -> tuple:
    s = schema
    result, error = s.dump(data)
    return result, error


def covert_msg(email_str):
    name, addr = parseaddr(email_str)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def email_msg(request, to_addr, username, hash_str):
    config_msg = request.app.config.EMAIL
    try:
        url = 'http://' + str(request.host) + '/confirm/' + hash_str
        connent = "<html><body>Hello, {}, Click <a href='{}'>Here</a>To " \
                  "Confirm Your Account </body></html>.".format(username, url)

        msg = MIMEText(connent, "html", "utf-8")

        from_addr = config_msg.get('from_addr')
        password = config_msg.get('password')
        smtp_server = config_msg.get('smtp_server')
        msg['From'] = covert_msg('Lome, {}'.format(from_addr))
        msg['To'] = covert_msg('<{}>'.format(to_addr))
        msg['Subject'] = Header('来自Lome', 'utf-8').encode()
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except (EOFError, IOError):
        status = None
        print('send Error')
    else:
        print('send success')
        status = True
    return status
