from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)

def generate_schema(json_data):
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for key, value in json_data.items():
        if isinstance(value, dict):
            schema["properties"][key] = generate_schema(value)
        elif isinstance(value, list):
            if len(value) > 0:
                schema["properties"][key] = {"type": "array", "items": generate_schema(value[0])}
            else:
                schema["properties"][key] = {"type": "array"}
        elif isinstance(value, int):
            schema["properties"][key] = {"type": "integer"}
        elif isinstance(value, float):
            schema["properties"][key] = {"type": "number"}
        elif isinstance(value, str):
            schema["properties"][key] = {"type": "string"}
        elif isinstance(value, bool):
            schema["properties"][key] = {"type": "boolean"}
        elif value is None:
            schema["properties"][key] = {"type": "null"}

        schema["required"].append(key)

    return schema


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data:
            schema = generate_schema(json_data)
            return jsonify(schema)
    return render_template('layout.html')