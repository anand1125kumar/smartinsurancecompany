import boto3
import random
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
import datetime

global username
global loginFlag


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to Smart Insurance Company, we offer a large variety insurance products at an affordable premium. I can help you to buy a policy online best suited to your needs. Would you like to proceed to buy a life insurance policy online or login to TCS bancs voice portal.").set_should_end_session(False)
        return handler_input.response_builder.response 



sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())


def handler(event, context):
    return sb.lambda_handler()(event, context)