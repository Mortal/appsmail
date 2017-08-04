import os
import time
import smtplib
import traceback
import aiosmtpd.controller


MAIL_FROM = os.environ['MAIL_FROM']
RELAY_HOST = os.environ['RELAY_HOST']
RELAY_PORT = int(os.environ['RELAY_PORT'])
RELAY_USER = os.environ['RELAY_USER']
RELAY_PASS = os.environ['RELAY_PASS']


class AppsMailServer:
    async def handle_MAIL(self, server, session, envelope, address, mail_options=()):
        if address != MAIL_FROM:
            return '500 Wrong sender; specify %r instead' % address
        envelope.mail_from = address
        envelope.mail_options.extend(mail_options)
        return '250 OK'

    # async def handle_RCPT(self, server, session, envelope, address, rcpt_options=()):
    #     envelope.rcpt_tos.append(address)
    #     envelope.rcpt_options.extend(rcpt_options)
    #     return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        try:
            conn = smtplib.SMTP(RELAY_HOST, RELAY_PORT)
            conn.login(RELAY_USER, RELAY_PASS)
            refused = conn.sendmail(envelope.mail_from,
                                    envelope.rcpt_tos,
                                    envelope.original_content)
            if refused:
                print(refused)
            print("To: %r" % (envelope.rcpt_tos,))
        except smtplib.SMTPException as exn:
            traceback.print_exc()
            return '550 SMTPException: %s' % exn


def main():
    controller = aiosmtpd.controller.Controller(
        AppsMailServer(), hostname='127.0.0.1', port=2525)
    controller.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        controller.stop()
    print("Done!")


if __name__ == '__main__':
    main()
