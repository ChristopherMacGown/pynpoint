import json
from pynpoint import providers

for provider in providers.load_providers():
    print json.dumps(provider.gather(), indent=4)
