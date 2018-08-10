{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang3082{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Riched20 10.0.17134}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\f0\fs22\lang10 # -*- coding: utf-8 -*-\par
""" simple fact sample app """\par
\par
from __future__ import print_function\par
\par
import random\par
\par
data = [\par
    "Don't wash your hair everyday, instead wash it 2 or 3 times a week to prevent dehydration.",\par
    "Pre-dry your hair with a microfiber towel once you step out of the shower."\par
]\par
SKILL_NAME = "Hair Care Tips"\par
GET_FACT_MESSAGE = "Here's your tip: "\par
HELP_MESSAGE = "You can say give me a tip, or, you can say exit... Would you like to hear one tip?"\par
HELP_REPROMPT = "  Would you like to hear another tip ?"\par
STOP_MESSAGE = "Alright, Goodbye!"\par
FALLBACK_MESSAGE = "The Hair Care Tips skill can't help you with that.  It can help you discover tips to take care of your hair. Would you like to hear a tip"\par
FALLBACK_REPROMPT = 'Would you like to hear a tip'\par
\par
# --------------- App entry point -----------------\par
\par
def lambda_handler(event, context):\par
    """  App entry point  """\par
\par
    #print(event)\par
\par
    if event['session']['new']:\par
        on_session_started()\par
\par
    if event['request']['type'] == "LaunchRequest":\par
        return on_launch(event['request'])\par
    elif event['request']['type'] == "IntentRequest":\par
        return on_intent(event['request'], event['session'])\par
    elif event['request']['type'] == "SessionEndedRequest":\par
        return on_session_ended()\par
\par
# --------------- Response handlers -----------------\par
\par
def on_intent(request, session):\par
    """ called on receipt of an Intent  """\par
\par
    intent_name = request['intent']['name']\par
\par
    # process the intents\par
    if intent_name == "givetip":\par
        return get_fact_response()\par
    elif intent_name == "AMAZON.YesIntent":\par
        return get_fact_response()\par
    elif intent_name == "AMAZON.NoIntent":\par
        return get_stop_response()\par
    elif intent_name == "AMAZON.HelpIntent":\par
        return get_help_response()\par
    elif intent_name == "AMAZON.StopIntent":\par
        return get_stop_response()\par
    elif intent_name == "AMAZON.CancelIntent":\par
        return get_stop_response()\par
    elif intent_name == "AMAZON.FallbackIntent":\par
        return get_fallback_response()\par
    else:\par
        print("invalid Intent reply with help")\par
        return get_help_response()\par
\par
def get_fact_response():\par
    """ get and return a random fact """\par
    randomFact = random.choice(data)\par
    cardcontent = randomFact\par
    speechOutput = GET_FACT_MESSAGE + randomFact + HELP_REPROMPT\par
\par
    return response(speech_response_with_card(SKILL_NAME, speechOutput,\par
                                                          cardcontent, False))\par
\par
\par
def get_help_response():\par
    """ get and return the help string  """\par
\par
    speech_message = HELP_MESSAGE\par
    return response(speech_response_prompt(speech_message,\par
                                                       speech_message, False))\par
def get_launch_response():\par
    """ get and return the help string  """\par
\par
    return get_fact_response()\par
\par
def get_stop_response():\par
    """ end the session, user wants to quit the game """\par
\par
    speech_output = STOP_MESSAGE\par
    return response(speech_response(speech_output, True))\par
\par
def get_fallback_response():\par
    """ end the session, user wants to quit the game """\par
\par
    speech_output = FALLBACK_MESSAGE\par
    return response(speech_response(speech_output, False))\par
\par
def on_session_started():\par
    """" called when the session starts  """\par
    #print("on_session_started")\par
\par
def on_session_ended():\par
    """ called on session ends """\par
    #print("on_session_ended")\par
\par
def on_launch(request):\par
    """ called on Launch, we reply with a launch message  """\par
\par
    return get_launch_response()\par
\par
\par
# --------------- Speech response handlers -----------------\par
\par
def speech_response(output, endsession):\par
    """  create a simple json response  """\par
    return \{\par
        'outputSpeech': \{\par
            'type': 'PlainText',\par
            'text': output\par
        \},\par
        'shouldEndSession': endsession\par
    \}\par
\par
def dialog_response(endsession):\par
    """  create a simple json response with card """\par
\par
    return \{\par
        'version': '1.0',\par
        'response':\{\par
            'directives': [\par
                \{\par
                    'type': 'Dialog.Delegate'\par
                \}\par
            ],\par
            'shouldEndSession': endsession\par
        \}\par
    \}\par
\par
def speech_response_with_card(title, output, cardcontent, endsession):\par
    """  create a simple json response with card """\par
\par
    return \{\par
        'card': \{\par
            'type': 'Simple',\par
            'title': title,\par
            'content': cardcontent\par
        \},\par
        'outputSpeech': \{\par
            'type': 'PlainText',\par
            'text': output\par
        \},\par
        'shouldEndSession': endsession\par
    \}\par
\par
def response_ssml_text_and_prompt(output, endsession, reprompt_text):\par
    """ create a Ssml response with prompt  """\par
\par
    return \{\par
        'outputSpeech': \{\par
            'type': 'SSML',\par
            'ssml': "<speak>" +output +"</speak>"\par
        \},\par
        'reprompt': \{\par
            'outputSpeech': \{\par
                'type': 'SSML',\par
                'ssml': "<speak>" +reprompt_text +"</speak>"\par
            \}\par
        \},\par
        'shouldEndSession': endsession\par
    \}\par
\par
def speech_response_prompt(output, reprompt_text, endsession):\par
    """ create a simple json response with a prompt """\par
\par
    return \{\par
        'outputSpeech': \{\par
            'type': 'PlainText',\par
            'text': output\par
        \},\par
        'reprompt': \{\par
            'outputSpeech': \{\par
                'type': 'PlainText',\par
                'text': reprompt_text\par
            \}\par
        \},\par
        'shouldEndSession': endsession\par
    \}\par
\par
def response(speech_message):\par
    """ create a simple json response  """\par
    return \{\par
        'version': '1.0',\par
        'response': speech_message\par
    \}\par
}
 