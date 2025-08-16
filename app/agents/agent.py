import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from dotenv import load_dotenv
load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "mumbai":
        return {
            "status": "success",
            "report": (
                "The weather in Mumbai is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "mumbai":
        tz_identifier = "Asia/Kolkata"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about time and weather.",
    instruction="You are a helpful agent who answers questions using up-to-date information. Use model knowledge and web if necessary.",
    tools=[google_search]
)

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="weather_app",
    session_service=session_service
)

# USER_ID = "user_weather"
SESSION_ID = "session_weather"

async def execute(request, USER_ID):
    """
    Executes a query against the agent and returns the final response.

    Args:
        query (str): The user's prompt.

    """
    await session_service.create_session(
        app_name="weather_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    message = types.Content(role="user", parts=[types.Part(text=f"{request['query']}. Answer in one single line by giving just the information asked and nothing more.")])
    try:
        final_response_text = ""
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
            if event.is_final_response():
                final_response_text = event.content.parts[0].text
                print("final resp",final_response_text)
                break
            
        return {"response": final_response_text}

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")
        return {"response": f"An unexpected error occurred: {e}"}