"""Routes for handling JSON Schema generation requests"""

from flask import Blueprint, render_template, request, jsonify
from json.decoder import JSONDecodeError  # Specific import for JSON parsing errors


bp = Blueprint('main', __name__)


def generate_schema(json_data, *, allow_empty_arrays=False):
    """Recursively generates a JSON Schema based on the provided JSON data

    Args:
        json_data (dict, list, str, int, float, bool, None): The JSON data to analyze
        allow_empty_strains (bool, optional): Flag to allow empty arrays with a specific schema. Defaults to False.

    Returns:
        dict: The generated JSON Schema representing the data structure
            or dict with error message and status code if invalid data is encountered.
    """

    schema = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }

    for key, value in json_data.items():
        try:
            if isinstance(value, dict):
                schema["properties"][key] = generate_schema(value)
            elif isinstance(value, list):
                if len(value) > 0:
                    schema["properties"][key] = {
                        "type": "array",
                        "items": generate_schema(value[0]),
                    }
                else:
                    if allow_empty_arrays:
                        schema["properties"][key] = {"type": "array", "items": None}
                    else:
                        schema["properties"][key] = {"type": "array"}
            elif isinstance(value, bool):
                schema["properties"][key] = {"type": "boolean"}
            elif isinstance(value, (int, float)):
                schema["properties"][key] = {"type": "number"}
            elif isinstance(value, str):
                schema["properties"][key] = {"type": "string"}
            elif value is None:
                schema["properties"][key] = {"type": "null"}
            schema["required"].append(key)
        except (TypeError, ValueError) as e:
            return {"error": f'Invalid JSON data for key "{key}": {str(e)}'}, 400

    return schema


@bp.route('/', methods=['GET', 'POST'])
def index():
    """Renders the main page and handles POST requests for schema generation

    Returns:
        str: Rendered HTML template (GET) or JSON response (POST)
    """

    if request.method == 'POST':
        try:
            json_data = request.get_json()
            if json_data:
                schema = generate_schema(json_data)
                return jsonify(schema)
        except (JSONDecodeError, TypeError, ValueError) as e:
            return jsonify({'error': f'Error parsing JSON data: {str(e)}'}), 400
    return render_template('layout.html')
