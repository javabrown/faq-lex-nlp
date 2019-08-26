@echo off

rem 1. aws lex-models put-slot-type --region us-east-1 --name iCWFAQSlotTypes --cli-input-json file://faq-slot-types.json
aws lex-models put-slot-type --region us-east-1 --name iCWFAQSlotTypes --cli-input-json file://parser/gen/slots.json
PING -n 1 127.0.0.1>nul

rem 2.1 aws lex-models put-intent --region us-east-1 --name iCWFAQIntents --cli-input-json file://faq-intents.json
aws lex-models put-intent --region us-east-1 --name iCWFAQIntents --cli-input-json file://parser/gen/intents.json
PING -n 1 127.0.0.1>nul

rem 2.2 aws lex-models put-intent --region us-east-1:
rem aws lex-models put-intent --region us-east-1 --name icwLoanEnquiry --cli-input-json file://parser/gen/intent-loan-enquiry.json


rem aws lex-models put-bot --region us-east-1 --name iCWFAQBot --cli-input-json file://faq-bot.json
rem PING -n 1 127.0.0.1>nul

rem aws lex-models get-bot --region us-east-1 --name iCWFAQBot --version-or-alias "/$LATEST"