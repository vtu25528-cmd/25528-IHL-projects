from openai import OpenAI
from tools import calculator
import json


# Connect to LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


# Change this to the model identifier shown by LM Studio
MODEL = "your-model"


# Tool definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation to perform"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    }
]


def run_agent(user_input):

    messages = [
        {
            "role": "user",
            "content": user_input
        }
    ]

    # First request to the LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Add the assistant's response to conversation
    messages.append(message)

    # Check whether the model requested a tool
    if message.tool_calls:

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Execute the requested Python tool
            if function_name == "calculator":

                result = calculator(
                    arguments["a"],
                    arguments["b"],
                    arguments["operation"]
                )

            else:
                result = "Unknown tool"

            # Send tool result back to the LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

        # Ask the LLM for the final answer
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        return final_response.choices[0].message.content

    else:

        # Model answered without using a tool
        return message.content


if __name__ == "__main__":

    question = input("Ask Agent: ")

    answer = run_agent(question)

    print("\nAgent:", answer)