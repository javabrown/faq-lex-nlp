rem  -----------------------------------------------------

rem --DELETE BOT--
aws lex-models delete-bot --region us-east-1 --name iCWFAQBot
PING -n 5 127.0.0.1>nul

rem --DELETE Intent
aws lex-models delete-intent --region us-east-1 --name iCWFAQIntents
PING -n 5 127.0.0.1>nul

rem --DELETE Slot-Type
aws lex-models delete-slot-type --region us-east-1 --name iCWFAQSlotTypes
PING -n 5 127.0.0.1>nul

rem  -----------------------------------------------------

aws lex-models put-slot-type --region us-east-1 --name iCWFAQSlotTypes --cli-input-json file://faq-slot-types.json
PING -n 1 127.0.0.1>nul

aws lex-models put-intent --region us-east-1 --name iCWFAQIntents --cli-input-json file://faq-intents.json
PING -n 1 127.0.0.1>nul

rem aws lex-models put-bot --region us-east-1 --name iCWFAQBot --cli-input-json file://faq-bot.json
rem PING -n 1 127.0.0.1>nul

rem aws lex-models get-bot --region us-east-1 --name iCWFAQBot --version-or-alias "/$LATEST"