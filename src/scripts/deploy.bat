aws lex-models put-bot --region us-east-1 --name iCWFAQBot --cli-input-json file://faq-bot.json
PING -n 5 127.0.0.1>nul

aws lex-models get-bot --region us-east-1 --name iCWFAQBot --version-or-alias "$LATEST"
