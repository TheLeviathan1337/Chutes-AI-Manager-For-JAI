import aiohttp
import json

async def fetch_chute(api_token, model_config, message_history, is_stream):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }

    body = {
        "model": model_config.model_name,
        "messages": message_history,
        "stream": is_stream,
        "max_tokens": model_config.max_tokens,
        "temperature": model_config.temperature,
    }

    async with aiohttp.ClientSession() as session:
        # Create boolean buffer_content to track if we are currently buffering content
        buffer_content = False
        # Create boolean safe_override to quantify if we no longer have to worry about reasoning tokens
        safe_override = True
        # If we have reasoning tokens expected, set safe override to False because we haven't resolved the issue with reasoning tokens
        if model_config.start_reasoning_token is not None and model_config.end_reasoning_token is not None:
            safe_override = False
        # Initialize empty buffer
        buffer = ""

        async with session.post(
            "https://llm.chutes.ai/v1/chat/completions",
            headers=headers,
            json=body
        ) as response:
            async for line in response.content:
                line = line.decode("utf-8").strip()

                if not line or not line.startswith("data:"):
                    continue

                if line == "data: [DONE]":
                    break
  
                # If we are actively buffering content, run this logic
                if buffer_content:
                    # Try to add data to the buffer
                    try:
                        data = json.loads(line[6:])
                        content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if not content:
                            continue
                        buffer += content
                        #Uncomment to DEBUG buffer
                        #print("NEW BUFFER BELOW")
                        #print(buffer)
                    except:
                        pass
                    # If the buffer ends with the reasoning token, we no longer need to buffer content.
                    if buffer.endswith(model_config.end_reasoning_token):
                        # Set buffer_content to False because we are done buffering and tracking
                        buffer_content = False
                        # Set safe_override to True because we specifically found an end to the reasoning, meaning we no longer will ever have to watch for reasoning tokens
                        safe_override = True
                # Otherwise, go here
                else:
                    # If we have reasoning tokens to check for, and safe_override is False, it means that we need to identify the start of the reasoning tokens
                    if model_config.start_reasoning_token is not None and safe_override == False:
                        try:
                            data = json.loads(line[6:])
                            content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if not content:
                                continue
                            buffer += content
                            #Uncomment to DEBUG buffer
                            #print("NEW BUFFER BELOW")
                            #print(buffer)
                        except:
                            pass
                        
                        # Check if there's only one possible reasoning token
                        if type(model_config.start_reasoning_token) == str:
                            # If the buffer starts with the beginning of the reasoning tokens, then we know to start buffering content and checking for the end of the reasoning tokens
                            if buffer.startswith(model_config.start_reasoning_token):
                                buffer_content = True
                            # If the reasoning tokens weren't identified, just stream data
                            else:
                                yield f"{line}\n\n"
                        # Else there is multiple possible start tokens
                        else:
                            # Check every token
                            for possible_token in model_config.start_reasoning_token:
                                # If the token is found, start buffering content
                                if buffer.startswith(possible_token):
                                    buffer_content = True
                                    break
                            # Stream data if no token caught
                            if not buffer_content:
                                yield f"{line}\n\n"
                    # If we don't have to concern ourselves with reasoning tokens at all, just stream data
                    else:
                        yield f"{line}\n\n"

                