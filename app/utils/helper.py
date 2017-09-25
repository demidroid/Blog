
def request_loads(request, schema) -> tuple:
    args = request.args or dict()
    s = schema()
    if request.json:
        args.update(request.json)
    data, error = s.load(args)
    return data, error


def data_dumps(data, schema) -> tuple:
    s = schema
    result, error = s.dumps(data)
    return result, error
