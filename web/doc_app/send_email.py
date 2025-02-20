import smtplib


def send_notification(receive_email, name, surname):
    email = 'lyceum1Docs@yandex.ru'
    password = 'ukuscrtzkvmiimvs'

    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)

    subject = 'Ваша справка об обучении'
    email_text = (f'Здравствуйте, {name} {surname}\n'
                  f'Ваша справка об обучении в Лицее № 1 готова')
    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email, receive_email, subject, email_text)

    server.set_debuglevel(1)
    server.sendmail(email, receive_email, message)
    server.quit()









