@echo off

rem 1. --DELETE BOT--
aws lex-models delete-bot --region us-east-1 --name iCWFAQBot
PING -n 5 127.0.0.1>nul


rem 2.1 --DELETE Intent
aws lex-models delete-intent --region us-east-1 --name iCWFAQIntents

PING -n 5 127.0.0.1>nul

rem 3. --DELETE Slot-Type
aws lex-models delete-slot-type --region us-east-1 --name iCWFAQSlotTypes
PING -n 5 127.0.0.1>nul
