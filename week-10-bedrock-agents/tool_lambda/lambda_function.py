import json
import math

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    action_group = event.get('actionGroup')
    function = event.get('function')
    parameters = event.get('parameters', [])
    params = {p['name']: p['value'] for p in parameters}
    
    if function == "calculator":
        expression = params.get('expression', '')
        try:
            result = eval(expression, {"__builtins__": {}}, {
                "sqrt": math.sqrt,
                "pow": math.pow,
                "abs": abs,
                "round": round
            })
            response_body = str(result)
        except Exception as e:
            response_body = f"Error: {str(e)}"
    else:
        response_body = f"Unknown function: {function}"
    
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,
            "function": function,
            "functionResponse": {
                "responseBody": {
                    "TEXT": {
                        "body": response_body
                    }
                }
            }
        }
    }