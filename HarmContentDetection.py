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

analyze_request = {
  'comment': { 'text': 'world is beuatiful' },
  'requestedAttributes': {'PROFANITY': {}, "TOXICITY" : {}, "SEVERE_TOXICITY" :{}, "IDENTITY_ATTACK" : {}, "INSULT" :{}, "THREAT" : {}}
}

response = client.comments().analyze(body=analyze_request).execute()
print(json.dumps(response, indent=2))