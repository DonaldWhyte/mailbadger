class Validator:

    def validate(self, address):
        raise NotImplementedError('validate() invoked on base class')

    def validate_mail_server(self, domain):
        raise NotImplementedError('validate_mail_server() invoked on base class')
