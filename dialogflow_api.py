import uuid

from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session


def run_sample():
    # TODO(developer): Update these values when running the function
    # project_id = "YOUR-PROJECT-ID"
    # location = "YOUR-LOCATION-ID"
    # agent_id = "YOUR-AGENT-ID"
    # event = "YOUR-EVENT"
    # language_code = "YOUR-LANGUAGE-CODE"

    project_id = "gen-ai-guru-live-lecture"
    location = "global"
    agent_id = "539a1983-6650-47a9-a78b-18fd4b9e9ccc"
    event = "sys.no-match-default"
    language_code = "en-us"

    detect_intent_with_event_input(
        project_id,
        location,
        agent_id,
        event,
        language_code,
    )


def detect_intent_with_event_input(
    project_id,
    location,
    agent_id,
    event,
    language_code,
):
    """Detects intent using EventInput"""
    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())
    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )

    # Construct detect intent request:
    event = session.EventInput(event=event)
    query_input = session.QueryInput(event=event, language_code=language_code)
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
    )

    response = session_client.detect_intent(request=request)
    response_text = response.query_result.response_messages[0].text.text[0]
    print(f"Response: {response_text}")
    return response_text

run_sample()