from flask import Flask, request, jsonify
from flatten_json import flatten
import requests
import json
import os
import importlib

app = Flask(__name__)

WEBHOOK_PROXY_DEBUG="false"
WEBHOOK_PROXY_DEBUG_JSON_DUMPS="false"
WEBHOOK_PROXY_DEBUG_INDENT=2
WEBHOOK_PROXY_TRANSFORMER="UNDEFINE"
REWRITE_ENDPOINT="http://localhost:5000/transformed"
 
@app.route('/webhook', methods=['POST'])
def webhook():
    raw = request.json
    debugPrint("recevied:" + debugJsonDumps(raw))
    
    transformed = transform(raw)
    debugPrint("transformed: " + debugJsonDumps(transformed))

    response = transferWith(transformed)
    debugPrint("responseAfterRePOST: " + debugJsonDumps(response.json()))

    return jsonify({"status": "success", "response": response.json()}), response.status_code

@app.route('/transformed', methods=['POST'])
def transformed():
    return jsonify(request.json), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "WEBHOOK_PROXY_DEBUG": str(os.getenv('WEBHOOK_PROXY_DEBUG', WEBHOOK_PROXY_DEBUG)),
        "WEBHOOK_PROXY_DEBUG_JSON_DUMPS": str(os.getenv('WEBHOOK_PROXY_DEBUG_JSON_DUMPS', WEBHOOK_PROXY_DEBUG_JSON_DUMPS)),
        "WEBHOOK_PROXY_DEBUG_INDENT": str(os.getenv('WEBHOOK_PROXY_DEBUG_INDENT', WEBHOOK_PROXY_DEBUG_INDENT)),
        "WEBHOOK_PROXY_TRANSFORMER": str(os.getenv('WEBHOOK_PROXY_TRANSFORMER', WEBHOOK_PROXY_TRANSFORMER)),
        "REWRITE_ENDPOINT": os.getenv('REWRITE_ENDPOINT', REWRITE_ENDPOINT)
    }), 200

def debugJsonDumps(raw):
    if os.getenv('WEBHOOK_PROXY_DEBUG_JSON_DUMPS', WEBHOOK_PROXY_DEBUG_JSON_DUMPS) == "true":
        return json.dumps(raw, indent=WEBHOOK_PROXY_DEBUG_INDENT, ensure_ascii=False)
    return str(flatten(raw))

def debugPrint(msg):
    if os.getenv('WEBHOOK_PROXY_DEBUG', WEBHOOK_PROXY_DEBUG) == "true":
        print(msg)
    else:
        return

def transform(raw):
    transformerModule=os.getenv('WEBHOOK_PROXY_TRANSFORMER', WEBHOOK_PROXY_TRANSFORMER)
    if transformerModule != WEBHOOK_PROXY_TRANSFORMER:
        return importlib.import_module(transformerModule).transform(raw)
    else:
        return raw

def transferWith(payload):
    rewriteEndpoint=os.getenv('REWRITE_ENDPOINT', REWRITE_ENDPOINT)
    debugPrint('Re-POST to ' + rewriteEndpoint)
    return requests.post(rewriteEndpoint, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)