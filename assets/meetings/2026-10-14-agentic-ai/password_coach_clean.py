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

COMMON = {"password", "123456", "123456789", "qwerty", "letmein", "iloveyou", "admin", "welcome1", "password1","mucsc"}


def check_strength(password: str) -> str:
    """Measure a password: its length and how many character types it uses."""
    types = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    ]
    return f"length {len(password)}, uses {sum(types)} of 4 character types"


def is_common(password: str) -> str:
    """Check whether a password is on the list attackers try first."""
    if password.lower() in COMMON:
        return "COMMON: attackers try this one first"
    return "not on the common list"


def make_password(length: int = 16) -> str:
    """Generate a new random password with the given number of characters."""
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(secrets.choice(alphabet) for _ in range(min(int(length), 64)))


TOOLS = {tool.__name__: tool for tool in (check_strength, is_common, make_password)}
messages = [{"role": "system", "content": PROMPT}]

while True:
    # Get a question from the user and add it to the messages.
    question = input("\nyou> ")
    if question == "quit":
        break
    messages.append({"role": "user", "content": question})

# Run the coach for a few steps, then stop if it doesn't call any tools.
    for step in range(6):
        reply = chat(model=MODEL, messages=messages, tools=list(TOOLS.values())).message
        messages.append(reply)
        # If the coach didn't call any tools, print its answer and stop.
        if not reply.tool_calls:
            print("coach>", reply.content)
            break
            # If the coach did call tools, run them and add their results to the messages.
        for call in reply.tool_calls:
            # Call the tool and add its result to the messages.
            name, args = call.function.name, call.function.arguments
            try:
                result = TOOLS[name](**args)
            except Exception as error:
                result = f"error: {error!r}"
            print(f"  [tool] {name}({args}) -> {result}")
            # Add the result to the messages so the coach can see it.
            messages.append({"role": "tool", "tool_name": name, "content": result})
    else:
        # If the coach didn't stop after 6 steps, it got stuck in a loop.
        print("coach> I got stuck in a loop. Try asking another way.")