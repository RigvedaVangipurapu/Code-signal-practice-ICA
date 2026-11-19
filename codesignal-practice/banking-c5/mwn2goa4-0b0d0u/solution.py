def solution(queries):

    operation, value = queries
    self.registry = []
    self.registry_lookup = set()

    if operation == 'CREATE':
        if value in registry_lookup:
            return "false"
        registry.append(value)
        registry_lookup = set(registry)
        return "true"
    
    if operation == 'GET':
        for i in range(len(registry)):
            if registry[i] == value:
                return str(i)
        return ""

    if operation == 'DELETE':
        if value in registry_lookup:
            registry.remove(value)
            registry_lookup = set(registry)
            return "true"
        else:
            return "false"

    else:
        return "false"


    results = []
    for query in queries:
        results.append(solution(query))
    return results
