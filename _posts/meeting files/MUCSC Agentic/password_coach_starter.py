"""
Password coach - your first AI agent.

Run:   python password_coach_starter.py      (Mac/Linux: python3)
Stop:  type quit
Use made-up passwords only. Never type a real one.
"""

import secrets
import string
from ollama import chat

MODEL = "llama3.2"

PROMPT = """You are a password coach for students who are new to cybersecurity.

You cannot judge a password by looking at it. Never guess its length or strength.
Use your tools to get the facts, then explain them.

- To judge a password, call check_strength and is_common with the exact password.
- To create a password, call make_password. Never invent one yourself.

A password is strong when it has at least 12 characters, uses at least 3 of the
4 character types, and is not common. Otherwise it is weak.

Answer in two or three short, plain sentences. Say strong or weak, and why."""

# Add a list of passwords you think are common. maybe look up a list on github
COMMON = {"password", "123456", "qwerty", "letmein", "iloveyou", "admin", "welcome1", "password1"}


# TODO 1: create a function that checks the strength of a password


# TODO 2: create a function that checks if a password is common


# TODO 3: create a function that makes a random password


# TODO 4: make a dictionary of your tools and a list to hold the messages


# TODO 5/6: write the chat loop that asks the user for a question
            #write the agent loop that lets the model use your tools
