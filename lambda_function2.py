import logging
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Olá Gurus da codificação!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Olá Renato, como posso te ajudar?"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Assistente APPIA", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("Olá, eu sou a ÁPPIA, sua assistente pessoal para instâncias automatizadas. \n       "
                      "Você pode me dizer um comando do tipo quantas instâncias estão ligadas  ou  desligar instâncias")
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Como posso te ajudar?", speech_text))
        return handler_input.response_builder.response

"""CLASSE NATIVA SEM CHAMADA"""
class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

"""CLASSE NATIVA SEM CHAMADA"""
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response

"""CLASSE NATIVA SEM CHAMADA"""
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Desculpe, tive um problema. Você pode tentar novamente?"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################



class GatherServersIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GatherServersIntent")(handler_input)

    def handle(self, handler_input):
	    # type: (HandlerInput) -> Response
        import boto3
        total_instance_count = 0
        client = boto3.client('ec2')
        ec2 = boto3.resource('ec2','us-east-1')
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instance_count = int(len([instance.id for instance in instances]))
        total_instance_count = total_instance_count + instance_count
        if total_instance_count > 0:
            if total_instance_count == 1:
                speech_text = f"Existe {total_instance_count} instância rodando."
            elif total_instance_count > 1:
                speech_text = f"Existem {total_instance_count} instâncias rodando."
        else:
            speech_text = "Não encontrei nenhuma instância rodando no momento. "
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Verificando instâncias", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class InstanceStatusIntentHandler(AbstractRequestHandler):
    def can_handle(service, option):
        # type: (HandlerInput) -> bool
        return is_intent_name("InstanceStatusIntent")(handler_input)
        
    def handle(service, option):
        #type: (HandlerInput) -> Response
        import boto3
        
        aws_regions = 'us-east-1'
        ec2 = boto3.resource('ec2', region_name=option)
        instances = ec2.instances.all()
        runningInst=[]
        stoppedInst=[]
        i= "None"
        j= "None"
        for i in instances:
            if i.state['Name'] == 'running':
                runningInst.append(i.id)
            elif i.state['Name'] == 'stopped':
                stoppedInst.append(i.id)
        for i in runningInst:
            j='\n'.join(runningInst)
        for i in stoppedInst:
            k='\n'.join(stoppedInst)
        speech_text = "Listando o status das suas instâncias "+option+"\n" "*Ligadas:* \n" +"```"+j+"```"+"\n *Paradas:* \n" + "```"+k+"```"
        
        handler_input.response_builder.speak(speech_text).set_card(
           SimpleCard("Status de Instâncias", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class TurnOnInstancesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TurnOnInstancesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        import boto3
        region_name = 'Norte da Virgínia'
        client = boto3.client('ec2')
        ec2 = boto3.resource('ec2', 'us-east-1')
        server_client = boto3.client('ec2', region_name='us-east-1')
        response = server_client.start_instances(InstanceIds=['i-0b78f89a03cc95e15'])
        speech_text = "OK, sua estação de trabalho está sendo ligada na região `"+region_name+"`"
       
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Ligando instância", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response
        

class TurnOffInstancesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TurnOffInstancesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        import boto3
        client = boto3.client('ec2')
        ec2 = boto3.resource('ec2', 'us-east-1')
        server_client = boto3.client('ec2', region_name='us-east-1')
        response = server_client.stop_instances(InstanceIds=['i-0b78f89a03cc95e15'])
        speech_text = "Até mais Renato! estou desligando sua instância de trabalho."
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Até logo, Renato", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response



    


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(GatherServersIntentHandler())
sb.add_request_handler(TurnOffInstancesIntentHandler())
sb.add_request_handler(TurnOnInstancesIntentHandler())
sb.add_request_handler(InstanceStatusIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()