from core.dm import csc, Pr, PTurn

INTRO_MESSAGE = 'Привет! Я чат-бот “Плеяды”, приятно познакомиться! ' \
                'Предлагаю ответить на несколько вопросов, чтобы начать работу.' \
                '\nНажмите "знакомство", чтобы начать.'


@csc.add_handler(priority=Pr.FALLBACK)
def fallback(turn: PTurn):
    if not turn.user_object.get('forms', {}).get('form1_informal'):
        turn.response_text = INTRO_MESSAGE
        turn.suggests.append('знакомство')
    elif not turn.user_object.get('forms', {}).get('form2'):
        turn.response_text = 'Привет! У меня есть ещё одна анкета - про навыки, которые вам нужны. ' \
                             'Если вы её готовы пройти, жмите "навыки"!'
        turn.suggests.append('навыки')
    else:
        turn.response_text = "У меня пока больше нет для вас контента. Напишите позднее, пожалуйста."


@csc.add_handler(priority=Pr.STAGE + Pr.EPSILON, regexp='забудь меня')
def forget_me(turn: PTurn):
    turn.response_text = 'Хорошо, я стёр вас из своей памяти. Можете начать заново.'
    turn.user_object = {}
