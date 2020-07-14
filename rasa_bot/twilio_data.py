import yaml

# load yml file to dictionary
credentials = yaml.load(open('./credentials.yml'))



class Twilio_Check:
    @classmethod
    def from_credentials(cls, credentials):
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
        '<account_id>',
        '<auth_token>',
        'whatsapp:+14155238886'
    )
if __name__="__main__":
    print(credentials)
    #creden=Twilio_Check()
    #Twilio_Check.from_credentials(credentials)