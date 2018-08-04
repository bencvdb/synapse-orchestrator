import os
import urllib
import json
import yaml
import subprocess32
import logging
import schema_salad.ref_resolver
import datetime as dt
from synorchestrator import wdl_parser
from six import itervalues
from past.builtins import basestring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def visit(d, op):
    """Recursively call op(d) for all list subelements and dictionary 'values' that d may have."""
    op(d)
    if isinstance(d, list):
        for i in d:
            visit(i, op)
    elif isinstance(d, dict):
        for i in itervalues(d):
            visit(i, op)


def heredoc(s, inputs_dict):
    import textwrap
    s = textwrap.dedent(s).format(**inputs_dict)
    return s[1:] if s.startswith('\n') else s


def get_yaml(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.load(f)
    except IOError:
        logger.exception("No file found.  Please create: %s." % filepath)


def save_yaml(filepath, app_config):
    with open(filepath, 'w') as f:
        yaml.dump(app_config, f)


def get_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except IOError:
        logger.exception("No file found.  Please create: %s." % filepath)


def save_json(filepath, app_config):
    with open(filepath, 'w') as f:
        json.dump(app_config, f, indent=4)


def ctime2datetime(time_str):
    return dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds  # noqa
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return '{}h:{}m:{}s'.format(hours, minutes, seconds)


def find_asts(ast_root, name):
        """
        Finds an AST node with the given name and the entire subtree under it.
        A function borrowed from scottfrazer.  Thank you Scott Frazer!

        :param ast_root: The WDL AST.  The whole thing generally, but really
                         any portion that you wish to search.
        :param name: The name of the subtree you're looking for, like "Task".
        :return: nodes representing the AST subtrees matching the "name" given.
        """
        nodes = []
        if isinstance(ast_root, wdl_parser.AstList):
            for node in ast_root:
                nodes.extend(find_asts(node, name))
        elif isinstance(ast_root, wdl_parser.Ast):
            if ast_root.name == name:
                nodes.append(ast_root)
            for attr_name, attr in ast_root.attributes.items():
                nodes.extend(find_asts(attr, name))
        return nodes


def get_wdl_inputs(wdl):
    """
    Return inputs specified in WDL descriptor, grouped by type.
    """
    wdl_ast = wdl_parser.parse(wdl.encode('utf-8')).ast()
    workflow = find_asts(wdl_ast, 'Workflow')[0]
    workflow_name = workflow.attr('name').source_string
    decs = find_asts(workflow, 'Declaration')
    wdl_inputs = {}
    for dec in decs:
        if isinstance(dec.attr('type'), wdl_parser.Ast) and 'name' in dec.attr('type').attributes:
            # dec_type = dec.attr('type').attr('name').source_string
            dec_subtype = dec.attr('type').attr('subtype')[0].source_string
            dec_name = '{}.{}'.format(workflow_name,
                                      dec.attr('name').source_string)
            wdl_inputs.setdefault(dec_subtype, []).append(dec_name)
        elif hasattr(dec.attr('type'), 'source_string'):
            dec_type = dec.attr('type').source_string
            dec_name = '{}.{}'.format(workflow_name,
                                      dec.attr('name').source_string)
            wdl_inputs.setdefault(dec_type, []).append(dec_name)
    return wdl_inputs


def get_packed_cwl(workflow_url):
    """
    Create 'packed' version of CWL workflow descriptor.
    """
    return subprocess32.check_output(['cwltool', '--pack', workflow_url])
