from dialogic.adapters import VkAdapter


class VA(VkAdapter):
    def make_response(self, **kwargs):
        resp = super(VA, self).make_response(**kwargs)
        # resp['dont_parse_links'] = 1
        return resp
