#!/usr/bin/env python3
"""
Fetch weather information using MCP's ddg-search server.
"""

import anthropic
import json


def get_weather(location: str) -> str:
    """
    Get weather information for a specified location using MCP ddg-search.

    Args:
        location: The location to get weather for (e.g., "London", "New York")

    Returns:
        Weather information as a string
    """
    client = anthropic.Anthropic()

    # Define the tool - ddg-search from MCP
    tools = [
        {
            "name": "ddg_search",
            "description": "Search the web using DuckDuckGo",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    ]

    # Create initial message
    messages = [
        {
            "role": "user",
            "content": f"Get the current weather for {location}. Search for weather information and provide the temperature, conditions, and forecast."
        }
    ]

    # Call Claude with tool use
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Process the response
    if response.stop_reason == "tool_use":
        # Extract tool call
        tool_call = next(
            (block for block in response.content if block.type == "tool_use"),
            None
        )

        if tool_call:
            print(f"Searching for: {tool_call.input.get('query')}")
            # In a real implementation, you would execute the tool here
            # For now, we'll show what would be searched
            return f"Weather search initiated for: {tool_call.input.get('query')}"

    # Extract text response
    text_response = next(
        (block.text for block in response.content if hasattr(block, "text")),
        "No weather information found"
    )

    return text_response


if __name__ == "__main__":
    # Example: Get weather for a location
    location = "San Francisco"
    print(f"Getting weather for {location}...\n")
    weather_info = get_weather(location)
    print(weather_info)
