import copy
from datetime import datetime

import dialogic
from dialogic.cascade import Cascade, Pr, DialogTurn
from dialogic.dialog import Context, Response
from dialogic.dialog_manager import TurnDialogManager


csc = Cascade()


class PTurn(DialogTurn):
    pass


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


form1 = FFDM('data/form1.yaml')

form_dms = [
    form1
]


@csc.add_handler(priority=Pr.STAGE)
def try_forms(turn: DialogTurn):
    for dm in form_dms:
        form_response = dm.try_to_respond(turn.ctx)
        if form_response:
            turn.response = form_response
            return


def make_dm(forms_collection):
    dm = TurnDialogManager(csc)
    for m in form_dms:
        m.forms_collection = forms_collection
    return dm
