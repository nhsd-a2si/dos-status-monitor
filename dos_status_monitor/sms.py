from twilio.rest import Client

from . import config, logger

sms_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def send_sms(to, sms_text):

    logger.info(f'Sending SMS notification to '
                f'{to}')

    message = sms_client.messages.create(
        to,
        body=sms_text,
        from_=config.TWILIO_FROM_NUMBER)

    logger.debug(message.sid)
