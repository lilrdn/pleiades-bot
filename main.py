import os
import logging

import sentry_sdk
import dialogic


from core.dm import FFDM
from misc.vk import VA


if os.getenv('SENTRY_DSN', None) is not None:
    sentry_sdk.init(os.environ['SENTRY_DSN'])


logging.basicConfig(level=logging.DEBUG)


HELP_MESSAGE = 'Привет! Я чат-бот “Плеяды”, приятно познакомиться! ' \
               'Предлагаю ответить на несколько вопросов, чтобы начать работу.' \
               '\nНапечатайте "знакомство", чтобы начать.'


if os.environ.get('MONGODB_URI'):
    db = dialogic.storage.database_utils.get_mongo_or_mock()
    forms_collection = db.get_collection('forms')
    storage = dialogic.session_storage.MongoBasedStorage(database=db)
    log_storage = dialogic.storage.message_logging.MongoMessageLogger(database=db, detect_pings=True)
else:
    storage = dialogic.storage.session_storage.FileBasedStorage(path='_tmp/sessions')
    log_storage = None
    forms_collection = None


manager = FFDM('data/form1.yaml', default_message=HELP_MESSAGE, forms_collection=forms_collection)


connector = dialogic.dialog_connector.DialogConnector(
    dialog_manager=manager,
    storage=storage,
    log_storage=log_storage,
    alice_native_state=False,
)
connector.adapters[dialogic.SOURCES.VK] = VA(suggest_cols=3)


handler = connector.serverless_alice_handler
server = dialogic.server.flask_server.FlaskServer(connector=connector)
app = server.app


if __name__ == '__main__':
    server.parse_args_and_run()
