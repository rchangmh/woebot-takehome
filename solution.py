import json

def generate_conversation_paths(lesson):
    root_route = get_root_route(lesson)
    return recurse_paths(lesson, route_id=root_route, paths=[])

def get_dict(json_path):
    with open(json_path, 'r', errors='ignore') as f:
        data = json.load(f)
        return data

def get_root_route(lesson):
    for route_id in lesson:
        if lesson[route_id]['tag'].endswith('start'):
            return route_id

def recurse_paths(lesson, route_id=None, dialog_path=[], paths=[]):
    dialog_path = dialog_path.copy() + [route_id]
    if lesson[route_id]['tag'] == 'bye':
        paths += [dialog_path]
    else:
        routes = lesson[route_id]['routes'].split('|')
        for route_id in routes:
            if route_id not in dialog_path: # To prevent recursive loop.
                recurse_paths(
                    lesson,
                    route_id=route_id,
                    dialog_path=dialog_path,
                    paths=paths,
                )
    return paths

def reached_endpoint(lesson, route_id):
    paths = generate_conversation_paths(lesson)
    for path in paths:
        if route_id in path:
            for step_id in path:
                if lesson[step_id]['stage'] == 'endpoint':
                    return True
                elif route_id == step_id:
                    return False
    return False


LABELS = get_dict('./labels.json')
ALLORNOTHING = get_dict('./allornothing.json')

print(generate_conversation_paths(LABELS))
assert(reached_endpoint(LABELS, 'LUU') == False)
assert(reached_endpoint(LABELS, 'EQC') == False)
assert(reached_endpoint(LABELS, 'GYU') == True)
assert(reached_endpoint(LABELS, 'VNT') == True)
assert(reached_endpoint(LABELS, 'ANG') == True)
assert(reached_endpoint(LABELS, 'XQP') == False)
assert(reached_endpoint(LABELS, 'UCH') == True)

print(generate_conversation_paths(ALLORNOTHING))
assert(reached_endpoint(ALLORNOTHING, 'EIC') == False)
assert(reached_endpoint(ALLORNOTHING, 'TUD') == False)

