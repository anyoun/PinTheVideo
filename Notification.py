from pushover import Client

def send(title, message, options):
    if options['pushover']['enable']:
        client = Client(options['pushover']['user'], api_token=options['pushover']['apiToken'])
        client.send_message(message, title=title, priority=-1)
