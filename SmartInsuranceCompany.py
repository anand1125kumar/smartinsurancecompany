import boto3
ddb = boto3.client("dynamodb")
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
        handler_input.response_builder.speak("Welcome to Smart Insurance Company, we offer a large variety of insurance products at an affordable premium. I can help you to buy a policy online best suited to your needs. Would you like to proceed to buy a life insurance policy online or login to Smart Insurance Company voice portal.").set_should_end_session(False)
        return handler_input.response_builder.response


################################# I would like yo buy a policy online ##################################################################################
class appNumberIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("appNumberIntent")(handler_input)

    def handle(self, handler_input):

         ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)

    ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        if(status == 'True'):
        #####################################################################
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                uwrflag = str(data['Item']['underwritingflag'])
                
                if(uwrflag == "no"):
                    speakText = "Would you like to capture your pending underwriting details?"

                else:
                    speakText = "How may I help you?"             

            except BaseException as e:
                print(e)
                raise(e)
        else:
                speakText = "Please enter valid username and pin for successfull login."


        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#############################################################################################################################

class RegisterUserIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterUserIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Great!, Please tell what should be your user name for online registration").set_should_end_session(False)
        return handler_input.response_builder.response

###############################################################################################################################


############################### My user name for registration should be ****** #############################################
class RegisterUserNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterUserNameIntent")(handler_input)

    def handle(self, handler_input):
        
        username = handler_input.request_envelope.request.intent.slots['username'].value
        username = str(username.lower())
       

##################################### verify existing user #####################################################################

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Login')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except Exception:
            status = 'inactive'
            
              
        try: 
            status = data1['Item']['status']
            status = status.lower()

        except Exception:
            status = 'inactive'


#######################################################################################################################################

        if status != 'active':

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Log')
                data1 = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Login')
                data1 = table.put_item(
                    Item={
                        'username': username,
                        'status': 'active'
                        
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Temp')
                data1 = table.put_item(
                    Item={
                        'username': username,
                        'status': 'True',
                        'tempfield':'null'
                        
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)



            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data1 = table.put_item(
                    Item={
                        'username': username
                        
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

            speak_text = "OK, Please set your 4 digit pin"


        else:
            speak_text = 'username already exists, please try some other username'


        handler_input.response_builder.speak(speak_text).set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################


############################### My pin should be ****** ####################################
class RegisterPasswordIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterPasswordIntent")(handler_input)

    def handle(self, handler_input):

        pin = handler_input.request_envelope.request.intent.slots['pin'].value

        ## Fetch username from log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        pin = str(pin)
    ##############################################################################

        try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Login')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set password=:pn",
                        ExpressionAttributeValues={':pn': pin}         
                                                
                    )

        except BaseException as e:
                print(e)
                raise(e)

        handler_input.response_builder.speak("OK, Please tell your full name").set_should_end_session(False)
        return handler_input.response_builder.response


########################################################################################################################



############################### My full name is ****** ####################################
class RegisterFullNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterFullNameIntent")(handler_input)

    def handle(self, handler_input):

        fullname = handler_input.request_envelope.request.intent.slots['fullname'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Login')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set fullname=:fn",
                    ExpressionAttributeValues={':fn': fullname}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("OK, Please tell your current city").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################

########################################################################################################################
############################### My current city is ****** ####################################
class RegisterCityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterCityIntent")(handler_input)

    def handle(self, handler_input):

        city1 = handler_input.request_envelope.request.intent.slots['city'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update city in bancs login table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Login')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set city=:ln",
                    ExpressionAttributeValues={':ln': str(city1)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("OK, please tell me how much insurance cover amount you want").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################



############################### Insurance cover amount should be ****** ####################################
class RegisterCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramount = handler_input.request_envelope.request.intent.slots['coveramount'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update cover amount  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set coveramount=:ca",
                    ExpressionAttributeValues={':ca': str(coveramount)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("OK, please tell me how much should be the term of the insurance").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################





############################### Insurance term should be ****** ####################################
class RegisterInsuranceTermIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("RegisterInsuranceTermIntent")(handler_input)

    def handle(self, handler_input):

        term = handler_input.request_envelope.request.intent.slots['term'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update cover amount  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set term=:ca",
                    ExpressionAttributeValues={':ca': int(term)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        ############################ fetch cover amount    #####################

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Policy_Details')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        coveramount = data1['Item']['coveramount']

        coveramount = int(coveramount)
        term = int(term)

        policynumber = random.randint(100000000000,999999999999)
        #policynumber = '112211221122'
        premiumamount = coveramount/(term*120)
        premiumamount = "{:.2f}".format(premiumamount)

        today = datetime.datetime.today()
        

        dd = "05"
        mm = int(today.month)
        yy = int(today.year)

        if(mm < 12):
            mm = mm + 1
        else:
            mm = 1
            yy = yy + 1

        mm =str(mm)
        yy = str(yy)

        nextduedate = dd+"-"+mm+"-"+yy
        today = str(today.day) +"-"+ str(today.month) +"-"+ str(today.year)
        
        ## update policy number  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set policynumber=:pn, premiumamount=:pa, premiumduedate=:pdd, advisorname=:adv, appnumber=:appno, underwritingflag=:uwrflag, uwrquest1=:uwrq1, uwrquest2=:uwrq2, uwrquest3=:uwrq3, uwrquest4=:uwrq4, uwrquest5=:uwrq5, uwrquest6=:uwrq6, uwrquest7=:uwrq7, uwrquest8=:uwrq8, uwrquest9=:uwrq9, uwrquest10=:uwrq10, uwrquest11=:uwrq11, uwrquest12=:uwrq12, uwrquest13=:uwrq13, uwrquest14=:uwrq14, uwrquest15=:uwrq15, uwrquest16=:uwrq16, uwrquest17=:uwrq17, uwrquest18=:uwrq18, uwrquest19=:uwrq19, uwrans1=:uwra1, uwrans2=:uwra2, uwrans3=:uwra3, uwrans4=:uwra4, uwrans5=:uwra5, uwrans6=:uwra6, uwrans7=:uwra7, uwrans8=:uwra8, uwrans9=:uwra9, uwrans10=:uwra10, uwrans11=:uwra11, uwrans12=:uwra12, uwrans13=:uwra13, uwrans14=:uwra14, uwrans15=:uwra15, uwrans16=:uwra16, uwrans17=:uwra17, uwrans18=:uwra18, uwrans19=:uwra19",
                    ExpressionAttributeValues={':pn': str(policynumber), ':pa': str(premiumamount), ':pdd': nextduedate, ':adv': 'Alexa Advisor', ':appno': str(policynumber), ':uwrflag': 'no', ':uwrq1': 'Will your occupation require you to travel or stay outside of the border of South Africa or Namibia for a period of one month each year?',':uwrq2': 'Do you on a regular basis participate in or plan to participate in any risky activities or sports with a higher than average risk of accident or injury example motor racing, climbing, aviation, combat sports, water sports etc.',':uwrq3': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, heart disease, for example, a stent, angioplasty, heart bypass, chest pain, irregular heartbeat, valve disorder, or deep vein thrombosis?',':uwrq4': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Brain disease for example a stroke, paralysis, parkinson\'s disease, bening brain tumour, multiple sclerosis or cerebral palsy?',':uwrq5': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Digestive system disease for example heartburn, stomach ulcer, crohn\'s disease, ulcerative colitis, hepatitis, fatty liver or pancreatitis?', ':uwrq6': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Pain or injury to your spine or neck for example a slipped disc, whiplasin, a trapped nerve or diseases of the spine?', ':uwrq7': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Amputation or loss of use of your limbs, fracture to any part of your body or bone deformities?',':uwrq8': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Pain or injury to your joints, muscles or tendons, for example, orthritis, osteoporosia, fibromyalgia, corpal tunnel syndrome or gout?',':uwrq9': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about, Mental disorder for example, depression, bi polar mood disorder, anxiety disorder or Paa traumatic disorder.', ':uwrq10': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about Dengue?', ':uwrq11': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about Cholesterol?', ':uwrq12': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about High or Low blood pressure?', ':uwrq13': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about Heart attack?', ':uwrq14': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about Diabetes?', ':uwrq15': 'Do you have, have you ever had or are you intending to see a doctor or a health professional about Asthma?', ':uwrq16': 'Have you ever tested HIV( Human Immunodeficiency Virus) positive?', ':uwrq17': 'Do you smoke or have you ever smoked or used any tobacco, nicotine or any nicotine substitution products?', ':uwrq18': 'Have you ever been tested positive, received treatment for or are you currently using any of the following, recreational drugs, for example, daggo, cocaine, amphetamines( tik, CAT), ecstoay - Anti-depression or sedatives - Performance enhancing substances for example, anabolic steroids - Or any other addictive substances?', ':uwrq19': 'Do you drink alcohol?', ':uwra1': 'null', ':uwra2': 'null', ':uwra3': 'null', ':uwra4': 'null', ':uwra5': 'null', ':uwra6': 'null', ':uwra7': 'null', ':uwra8': 'null', ':uwra9': 'null', ':uwra10': 'null', ':uwra11': 'null', ':uwra12': 'null', ':uwra13': 'null', ':uwra14': 'null', ':uwra15': 'null', ':uwra16': 'null', ':uwra17': 'null', ':uwra18': 'null', ':uwra19': 'null'}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)



        handler_input.response_builder.speak("Congratulations, you have successfully purchased a policy from world leading insurance company today, the  "+str(today)+", we will provide the best in class insurance services, your policy number is "+str(policynumber)+", your premium amount is "+str(premiumamount)+" rupees and your next premium due is on "+str(nextduedate)+", Please let me know if you need any other services. Thank you").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################


#########################################################################################################################
class LoginIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LoginIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Please tell your user name").set_should_end_session(False)
        return handler_input.response_builder.response


class searchappIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("searchappIntent")(handler_input)

    def handle(self, handler_input):
        ## Fetch username from Bancs_log table##############################
        


        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)

        username = data1['Item']['username']
        username = str(username)
        #print(username)

        if(username != 'null'):
            
        ##### FETCH login status ########################
                       
            speak_text = "Please tell your app number"         

        else:
            speak_text = "Please login to Smart Insurance Company portal"   

        
        handler_input.response_builder.speak(speak_text).set_should_end_session(False)
        return handler_input.response_builder.response


class UserNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("UserNameIntent")(handler_input)

    def handle(self, handler_input):
        username = handler_input.request_envelope.request.intent.slots['username'].value
        username = username.lower()
        try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Log')
                data1 = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
        except BaseException as e:
               print(e)
               raise(e)

        handler_input.response_builder.speak("Please tell your pin").set_should_end_session(False)
        return handler_input.response_builder.response



##################################################################################################################
##################################################################################################################

###########################################################################################################################


###########################################################################################################################
class captureunderwritingsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("captureunderwritingsIntent")(handler_input)

    def handle(self, handler_input):

        uwrdecision = handler_input.request_envelope.request.intent.slots['uwrflag'].value
        uwrdecision = uwrdecision.lower()
        
        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)


        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Policy_Details')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        uwrquest1 = data1['Item']['uwrquest1']
        uwrquest1 = str(uwrquest1)
    ####################################################

        #####################################################################
        if(status == 'True'):
            if(uwrdecision == 'yes'):
                speakText = uwrquest1
            #speakText = "Will your occupation require you to travel or stay outside of the border of South Africa or Namibia for a period of one month each year?"
                
                try:
                        dynamodb = boto3.resource('dynamodb')
                        table = dynamodb.Table('Temp')
                        data = table.update_item(
                        Key={
                            'username': username
                            },
                            UpdateExpression="set tempfield=:ca",
                            ExpressionAttributeValues={':ca': 'uwrquest1'}         
                                                
                        )


                except BaseException as e:
                        print(e)
                        raise(e)




            else:
                speakText = "It's okay, how may I help you?"
                try:
                    dynamodb = boto3.resource('dynamodb')
                    table = dynamodb.Table('Temp')
                    data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set tempfield=:ca",
                        ExpressionAttributeValues={':ca': 'null'}         
                                                
                    )

                except BaseException as e:
                        print(e)
                        raise(e)

            
        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################


class answerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("answerIntent")(handler_input)

    def handle(self, handler_input):

        answer = handler_input.request_envelope.request.intent.slots['ans'].value
        answer = answer.lower()
        
        

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)


        
    ####################################################

        #####################################################################
        if(status == 'True'):
            
            #speakText = "underwriting question 2."

                for i in range(1,20):

                    try:
                        dynamodb = boto3.resource('dynamodb')
                        table = dynamodb.Table('Policy_Details')
                        data1 = table.get_item(
                                Key={
                                        'username': username
                                    }
                                )
              
                    except BaseException as e:
                        print(e)
                        raise(e)    

                    uwraans = data1['Item']['uwrans'+str(i)]
                    uwraans = str(uwraans)

                    if(uwraans == 'null' or uwraans ==''):
               
                        try:
                        
                            k=str(i)
                            dynamodb = boto3.resource('dynamodb')
                            table = dynamodb.Table('Policy_Details')
                            data = table.update_item(
                                Key={
                                        'username': username
                                    },
                                UpdateExpression="set uwrans"+k+" =:ca",
                                ExpressionAttributeValues={':ca': answer}         
                                                
                                )

                        except BaseException as e:
                            print(e)
                            raise(e)

                        if(i != 19):
                            try:
                                dynamodb = boto3.resource('dynamodb')
                                table = dynamodb.Table('Policy_Details')
                                data1 = table.get_item(
                                    Key={
                                            'username': username
                                        }
                                    )
              
                            except BaseException as e:
                                print(e)
                                raise(e)    
                            xx= 'uwrquest'+str(i+1)
                            uwrq = data1['Item'][xx]
                            uwrq = str(uwrq)
                            speakText = uwrq

                        else:
                            speakText = "Your underwriting details have been saved successfully, thank you!"

                        

                       
                        if(i == 19):
                            
                            try:
                        
                            
                                dynamodb = boto3.resource('dynamodb')
                                table = dynamodb.Table('Policy_Details')
                                data = table.update_item(
                                    Key={
                                            'username': username
                                        },
                                    UpdateExpression="set underwritingflag =:ca",
                                    ExpressionAttributeValues={':ca': 'yes'}         
                                                
                                    )

                            except BaseException as e:
                                    print(e)
                                    raise(e)

                            testneeded = ""
                            for m in range(1,19):

                                try:
                                    dynamodb = boto3.resource('dynamodb')
                                    table = dynamodb.Table('Policy_Details')
                                    data1 = table.get_item(
                                        Key={
                                                'username': username
                                            }
                                        )
              
                                except BaseException as e:
                                    print(e)
                                    raise(e) 

                                uwrquestss = data1['Item']['uwrquest'+str(m)]
                                uwrquestss = str(uwrquestss)

                                uwraanss = data1['Item']['uwrans'+str(m)]
                                uwraanss = str(uwraanss)

                                if 'Cholesterol' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", Cholesterol Test"

                                if 'Dengue' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", Dengue Test"

                                if 'Diabetes' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", Diabetes Test"

                                if 'blood pressure' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", Blood pressure Test"

                                if 'Asthma' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", Asthma Test"

                                if 'HIV' in uwrquestss and uwraanss == 'yes':
                                    testneeded = testneeded+", HIV Test"

                            speakText = "Your underwriting details have been saved successfully, thank you!. You need to undergo the following medical tests"+testneeded



                            

                        break

                    

        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

######################################## 10-Oct-2020  #####################################################
class PremiumAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PremiumAmountIntent")(handler_input)


    #fetch premium amount
    

    def handle(self, handler_input):
        
        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)

    ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        if(status == 'True'):
        #####################################################################
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                premiumamount = str(data['Item']['premiumamount'])
                print(premiumamount)

                speakText = "Your next premium due amount is Rupees "+premiumamount

              
            except BaseException as e:
                print(e)
                raise(e) 
        else:
                speakText = "Please enter valid username and pin for successfull login."
        
        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response

###########################################################################################################

###########################################################################################################
###############################################  search app      ##########################################


#############################################################################################################
#BancsPINIntentHandler
#BancsLoginDetailsIntentHandler
class PINIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PINIntent")(handler_input)

    def handle(self, handler_input):

        pin = handler_input.request_envelope.request.intent.slots['pin'].value
        #pin = str(pin)
        #a = username.split(' and ')
        #b = a[1].replace("pin is ","")

        #username = a[0].lower()
        #pin = b
        #print(pin)

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
        except BaseException as e:
            print(e)
            raise(e)

        username = str(data['Item']['username'])
        

       # pin = handler_input.request_envelope.request.intent.slots['pin'].value
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Login')
            data = table.get_item(
                Key={
                    'username': username
                    }
            )
        except BaseException as e:
            print(e)
            raise(e)


        pinActual = str(data['Item']['password'])

        if(pin != pinActual):
            speech_text = "Invalid username and pin, please try again."
           # speech_text = "pin actual = "+pinActual+"pin entered = "+str(pin)
            loginFlag = 'False'
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Log')
                data = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   'null'
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

        else:
            speech_text = "Hello " + data['Item']['fullname'] + ". You have successfully logged in Smart Insurance Company portal, hope you are doing great, your current location is " + data['Item']['city'] + ".   How may I help you?"
            loginFlag = 'True'
        
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Log')
                data = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)


            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Temp')
                data = table.put_item(
                    Item={
                        'username': username,
                        'status':   loginFlag,
                        'tempfield': 'null'
                        }
                    )
            except BaseException as e:
                print(e)
                raise(e)

            

        #speech_text = username + "and" + b

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response  




#########  Fetch Premium Due Date   #######################################################################

class PremiumDueDateIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("PremiumDueDateIntent")(handler_input)

    def handle(self, handler_input):

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)

        #####################################################################
        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        if(status =='True'):

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                premiumduedate = data['Item']['premiumduedate']          
                speakText = "Your next premium due date is "+str(premiumduedate)

                     
            except BaseException as e:
                print(e)
                raise(e) 
        
        else:
            speakText = "Please enter valid username and pin for successfull login."

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################


#########  Fetch cover amount   #######################################################################

class ViewCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ViewCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                coveramount = str(data['Item']['coveramount'])
            

                speakText = "Your total insurance cover amount is Rupees "+coveramount

              
            except BaseException as e:
                print(e)
                raise(e) 

        else:
            speakText = "Please enter valid username and pin for successfull login."

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

#########  Increase cover amount   #######################################################################

class IncreaseCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("IncreaseCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramountincrease = handler_input.request_envelope.request.intent.slots['coveramountincrease'].value
        #coveramountincrease = str(coveramountincrease)

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )
                coveramount = data['Item']['coveramount']
                newCoverAmount = int(coveramount)+int(coveramountincrease)
                newCoverAmount = str(newCoverAmount)          

                speakText = "Ok Your insurance total cover amount has been successfully updated to Rupees "+newCoverAmount

                ########  Premium Calculation   #############
                insuranceTerm = int(data['Item']['term'])
                newCoverAmount = int(newCoverAmount)
                premiumamount = newCoverAmount/(insuranceTerm*120)
                premiumamount = "{:.2f}".format(premiumamount)
                ##############################################

            except BaseException as e:
                print(e)
                raise(e) 

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set coveramount=:ca, premiumamount = :pa",
                        ExpressionAttributeValues={':ca': str(newCoverAmount), ':pa': str(premiumamount)}         
                                                
                    )

            except BaseException as e:
                print(e)
                raise(e)


        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

#########  Decrease cover amount   #######################################################################

class DecreaseCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DecreaseCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramountdecrease = handler_input.request_envelope.request.intent.slots['decreasecoveramount'].value
        #coveramountdecrease = str(coveramountdecrease)

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )
                coveramount = data['Item']['coveramount']
                newCoverAmount = int(coveramount) - int(coveramountdecrease)
                newCoverAmount = str(newCoverAmount)          

                speakText = "OK, Your total insurance cover amount has been successfully updated to Rupees "+newCoverAmount

                ########  Premium Calculation   #############

                insuranceTerm = int(data['Item']['term'])
                newCoverAmount = int(newCoverAmount)
                premiumamount = newCoverAmount/(insuranceTerm*120)
                premiumamount = "{:.2f}".format(premiumamount)


                ##############################################

            except BaseException as e:
                print(e)
                raise(e) 

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Policy_Details')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set coveramount=:ca, premiumamount = :pa",
                        ExpressionAttributeValues={':ca': str(newCoverAmount), ':pa': str(premiumamount)}         
                                                
                    )

            except BaseException as e:
                print(e)
                raise(e)


        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again!!").set_should_end_session(False)
        return handler_input.response_builder.response

class LogoutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LogoutIntent")(handler_input)

    def handle(self, handler_input):


        #usname = Intent.slots.username.value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 

        #####################################################################

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Temp')
            data = table.put_item(
                Item={
                       'username': username,
                       'status':   'false',
                       'tempfield': 'null'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e)


        

            
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Log')
            data = table.put_item(
                Item={
                       'SerialNumber': '1',
                       'username': 'null'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("You have successfully logged out from Smart Insurance Company! Bye, take care of yourself, it was nice talking to you, I would like to meet you again.").set_should_end_session(True)
        return handler_input.response_builder.response


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(LoginIntentHandler())
sb.add_request_handler(UserNameIntentHandler())
sb.add_request_handler(searchappIntentHandler())
sb.add_request_handler(appNumberIntentHandler())
sb.add_request_handler(PremiumAmountIntentHandler())
sb.add_request_handler(PINIntentHandler())
sb.add_request_handler(captureunderwritingsIntentHandler())
sb.add_request_handler(RegisterCityIntentHandler())
sb.add_request_handler(PremiumDueDateIntentHandler())
sb.add_request_handler(ViewCoverAmountIntentHandler())
sb.add_request_handler(IncreaseCoverAmountIntentHandler())
sb.add_request_handler(DecreaseCoverAmountIntentHandler())
sb.add_request_handler(RegisterUserIntentHandler())
sb.add_request_handler(answerIntentHandler())
sb.add_request_handler(RegisterUserNameIntentHandler())
sb.add_request_handler(RegisterPasswordIntentHandler())
sb.add_request_handler(RegisterFullNameIntentHandler())
sb.add_request_handler(RegisterCoverAmountIntentHandler())
sb.add_request_handler(RegisterInsuranceTermIntentHandler())
sb.add_request_handler(LogoutIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)