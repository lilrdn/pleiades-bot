import copy
from datetime import datetime

import dialogic
from dialogic.dialog import Context, Response


class FFDM(dialogic.dialog_manager.FormFillingDialogManager):
    def __init__(self, *args, forms_collection=None, **kwargs):
        super(FFDM, self).__init__(*args, **kwargs)
        self.forms_collection = forms_collection

    def handle_completed_form(self, form, user_object, ctx: Context):
        document = copy.deepcopy(form)
        document['user_id'] = ctx.user_id
        document['timestamp'] = datetime.now()
        print('DOCUMENT IS', document)
        if self.forms_collection:
            self.forms_collection.insert_one(document)
        return Response(
            text=self.config.finish_message,
            user_object=user_object
        )
