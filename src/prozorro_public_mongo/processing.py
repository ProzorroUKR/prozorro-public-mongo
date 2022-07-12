

def filter_out_documents(data):
    recursive_filter_out_field(data=data, key="documents")


def recursive_filter_out_field(*_, key, data):
    if isinstance(data, dict):
        if key in data:
            data.pop(key)
    elif isinstance(data, list):
        for el in data:
            recursive_filter_out_field(key=key, data=el)
