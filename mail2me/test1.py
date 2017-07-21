#coding=utf-8

import smtplib
from email.mime.text import MIMEText


mailto_list=["409420873@qq.com"]
mail_host="smtp.blice.cn"  #设置服务器
mail_user="lyben@blice.cn"    #用户名
mail_pass="520521@libin"   #口令


def send_mail(to_list,sub,content):  #to_list：收件人；sub：主题；content：邮件内容
    me="<"+mail_user+">"   #显示发件人
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        print "邮件已发送！"
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == "__main__":
    send_mail(to_list=mailto_list,sub="测试",content="<h3>邮件收到</h3><br />测试没问题")