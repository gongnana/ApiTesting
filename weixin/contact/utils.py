import pystache


class Utils:
    @classmethod
    def template_parse(cls, template_path, dic):
        template = ''.join(open(template_path).readlines())
        return pystache.render(template, dic)
