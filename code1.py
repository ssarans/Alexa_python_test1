# -*- coding: utf-8 -*-
""" simple fact sample app """

from __future__ import print_function

import random

data = [
    "Don't wash your hair everyday, instead wash it 2 or 3 times a week to prevent dehydration.",
    "Pre-dry your hair with a microfiber towel once you step out of the shower.",
    "Limit your heat styling to once or twice a week."
]

SKILL_NAME = "Hair Care Tips"
GET_FACT_MESSAGE = "Here's your tip: "
HELP_MESSAGE = "You can say give me a tip, or, you can say exit... Would you like to hear one tip?"
HELP_REPROMPT = "  Would you like to hear another tip ?"
STOP_MESSAGE = "Alright, Goodbye!"
FALLBACK_MESSAGE = "The Hair Care Tips skill can't help you with that.  It can help you discover tips to take care of your hair. Would you like to hear a tip"
FALLBACK_REPROMPT = 'Would you like to hear a tip'

# --------------- App entry point -----------------

def lambda_handler(event, context):
    """  App entry point  """

    #print(event)

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']

    # process the intents
    if intent_name == "givetip":
        return get_fact_response()
    elif intent_name == "AMAZON.YesIntent":
        return get_fact_response()
    elif intent_name == "AMAZON.NoIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        print("invalid Intent reply with help")
        return get_help_response()

def get_fact_response():
    """ get and return a random fact """
    randomFact = random.choice(data)
    cardcontent = randomFact
    speechOutput = GET_FACT_MESSAGE + randomFact + HELP_REPROMPT

    return response(speech_response_with_card(SKILL_NAME, speechOutput,
                                                          cardcontent, False))


def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response():
    """ get and return the help string  """

    return get_fact_response()

def get_stop_response():
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")

def on_session_ended():
    """ called on session ends """
    #print("on_session_ended")

def on_launch(request):
    """ called on Launch, we reply with a launch message  """

    return get_launch_response()


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def dialog_response(endsession):
    """  create a simple json response with card """

    return {
        'version': '1.0',
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }

def speech_response_with_card(title, output, cardcontent, endsession):
    """  create a simple json response with card """

    return {
        'card': {
            'type': 'Simple',
            'title': title,
            'content': cardcontent
        },
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }
