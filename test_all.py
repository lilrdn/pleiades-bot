from dialogic.testing.testing_utils import make_context

from core.dm import make_dm
from scenarios import *  # noqa


def test_make_dm():
    dm = make_dm()
    ctx = make_context(text='начать', new_session=True)
    resp = dm.respond(ctx)
    assert resp
    assert 'бот' in resp.text
    assert 'начать' in resp.text
