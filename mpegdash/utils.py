from past.builtins import unicode   # python3 compat
from xml.dom import minidom
from datetime import datetime, timedelta
from isodate import parse_datetime, parse_duration, datetime_isoformat, duration_isoformat

import re


def _find_child_nodes_by_name(parent, name):
    nodes = []
    for node in parent.childNodes:
        # changed node.localName by node.tagName to support tag with prefix
        if node.nodeType == node.ELEMENT_NODE and node.tagName == name:
            nodes.append(node)
    return nodes


def parse_child_nodes(xmlnode, tag_name, node_type):
    elements = _find_child_nodes_by_name(xmlnode, tag_name)
    if not elements:
        return None

    nodes = []
    for elem in elements:
        if node_type in (unicode, str):
            node = xmlnode.firstChild.nodeValue
        else:
            node = node_type()
            node.parse(elem)
        nodes.append(node)

    return nodes


def parse_node_value(xmlnode, value_type):
    node_val = xmlnode.firstChild.nodeValue
    if node_val:
        return value_type(node_val)
    return None


def parse_attr_value(xmlnode, attr_name, value_type):
    if attr_name not in xmlnode.attributes.keys():
        return None

    attr_val = xmlnode.attributes[attr_name].nodeValue
    if isinstance(value_type, list):
        attr_type = type(value_type[0]) if len(value_type) > 0 else str
        return [attr_type(elem) for elem in re.split(r',| ', attr_val)]
    elif value_type is datetime:
        return parse_datetime(attr_val)
    elif value_type is timedelta:
        return parse_duration(attr_val)

    return value_type(attr_val)


def write_child_node(xmlnode, tag_name, node):
    if node:
        xmldoc = xmlnode if isinstance(xmlnode, minidom.Document) else xmlnode.ownerDocument
        if isinstance(node, list):
            for n in node:
                new_elem = xmldoc.createElement(tag_name)
                n.write(new_elem)
                xmlnode.appendChild(new_elem)
        else:
            new_elem = xmldoc.createElement(tag_name)
            node.write(new_elem)
            xmlnode.appendChild(new_elem)


def write_node_value(xmlnode, node_val):
    if node_val:
        xmldoc = xmlnode if isinstance(xmlnode, minidom.Document) else xmlnode.ownerDocument
        text_node = xmldoc.createTextNode(str(node_val))
        xmlnode.appendChild(text_node)


def write_attr_value(xmlnode, attr_name, attr_val):
    if attr_name and attr_val is not None:
        if isinstance(type(attr_val), list):
            attr_val = ' '.join([str(val) for val in attr_val])
        elif type(attr_val) is datetime:
            attr_val = datetime_isoformat(attr_val)
        elif type(attr_val) is timedelta:
            attr_val = duration_isoformat(attr_val)

        xmlnode.setAttribute(attr_name, str(attr_val))
