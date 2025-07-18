"""
email client
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from client.config import Config


class EmailClient:
    """
    发送邮件
    """

    def __init__(self, config):
        if config is None or config.properties['emailConfig'] is None:
            raise Exception('获取邮箱配置失败')
        config_ = config.properties['emailConfig']
        self.__sender = config_['sender']
        self.__sender_name = config_['sender_name']
        self.__receivers = config_['receivers']
        self.__receivers_name = config_['receivers_name']
        self.__host = config_['smtpHost']
        self.__port = config_['smtpPort']
        self.__auth_code = config_['authCode']
        self.__s = None
        self.__initial()

    def __initial(self):
        try:
            # 通过SSL方式发送，服务器地址和端口
            self.__s = smtplib.SMTP_SSL(self.__host, self.__port)
            # 登录邮箱
            self.__s.login(self.__sender, self.__auth_code)
            print('client initial success')
        except smtplib.SMTPException:
            print("client initial error")
            raise Exception("client initial error")

    def send(self, subject, content, receivers=None, receivers_name=None):
        receiver_name = receivers_name if receivers_name else self.__receivers_name
        # message = MIMEText(content, 'plain', 'utf-8')
        message = MIMEMultipart()
        # message['From'] = Header(self.__sender_name, 'utf-8')  # 发送者 
        message['From'] = formataddr((self.__sender_name, self.__sender))  # 发送者
        message['To'] = Header(receiver_name, 'utf-8')  # 接收者
        message['Subject'] = Header(subject, 'utf-8')

        message.attach(MIMEText(content, 'html'))

        receiver = receivers if receivers else self.__receivers
        try:
            self.__s.sendmail(self.__sender, receiver, message.as_string())
            print('send email success')
        except smtplib.SMTPException:
            print("send email error")
            raise Exception("send email error")


if __name__ == '__main__':
    config = Config()
    client = EmailClient(config)
    client.send("啦啦标题", "啦啦内容")
