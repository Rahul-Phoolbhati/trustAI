from googleapiclient import discovery
import json

API_KEY = 'AIzaSyAsXyKV32H990ll4npotKQtx4JGYRWe_8M'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)



# response = client.comments().analyze(body=analyze_request).execute()
# print(json.dumps(response, indent=2))


def check_harmful_content(text):
    analyze_request = {
        'comment': { 'text': text },
        'requestedAttributes': {'PROFANITY': {}, "TOXICITY" : {}, "SEVERE_TOXICITY" :{}, "IDENTITY_ATTACK" : {}, "INSULT" :{}, "THREAT" : {}}
    }
    try:
        response = client.comments().analyze(body=analyze_request).execute()
        print(json.dumps(response, indent=2))
        threshold = 0.4
        for attribute, scores in response['attributeScores'].items():
            if scores['summaryScore']['value'] > threshold:
                return True, attribute
        
        return False, None
    except Exception as e:
        print(f"Error checking content: {e}")
        return False, None