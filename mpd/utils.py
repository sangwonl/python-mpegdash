import re


def parse_attr_value(xmlnode, attr_name, def_val):
    val_type = type(def_val)
    if not xmlnode.attributes.has_key(attr_name):
        return val_type(def_val)

    attr_val = xmlnode.attributes[attr_name].nodeValue
    if type(def_val) == list:
        elem_type = type(def_val[0]) if len(def_val) > 0 else str
        return [elem_type(elem) for elem in re.split(',| ', attr_val)]

    return val_type(attr_val)


def parse_child_nodes(xmlnode, tag_name, node_type):
    tags = xmlnode.getElementsByTagName(tag_name)
    if not tags:
        return None

    nodes = []
    for tag in tags:
        if node_type == str:
            node = xmlnode.firstChild.nodeValue
        else:
            node = node_type()
            node.load(tag)
        nodes.append(node)

    return nodes


def parse_node_value(xmlnode, def_val):
    val_type = type(def_val)
    node_val = xmlnode.firstChild.nodeValue
    if node_val == '':
        return val_type(def_val)
    return val_type(node_val)
