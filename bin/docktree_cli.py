#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""
cli for docktree module
"""

from __future__ import print_function
import docktree
import sys
import json
import argparse
try:
    import argcomplete
except ImportError:
    pass


class ImageLayerEncoder(json.JSONEncoder):
    """JSON Encoder for ImageLayer objects"""

    def default(self, obj):
        """return a serializable version of obj
        :param obj: object to transform
        :return: serializable version of obj
        """
        if isinstance(obj, docktree.ImageLayer.ImageLayer):
            return {
                'identifier': obj.identifier,
                'children': obj.children,
                'parent_identifier':
                    obj.parent.identifier if obj.parent else '',
                'tags': obj.tags,
                'size': obj.size,
            }
        return json.JSONEncoder.default(self, obj)


def print_tree(heads, output_format='ascii'):
    """
    print a tree starting at heads to stdout
    :param heads: heads of the tree
    """
    if output_format == 'ascii':
        for head in heads:
            print(head.print_tree())
    elif output_format == 'json':
        print(json.dumps(heads, cls=ImageLayerEncoder))
    else:
        raise ValueError("invalid output_format '{0}'".format(output_format))


def parse_args(argv=sys.argv[1:]):
    """
    :param argv: arguments which we get called with
    :return: the parsed arguments as object (see argparse doc)
    :rtype: object
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-i',
        '--intermediate',
        action='store_true',
        dest='print_intermediate',
        default=False,
        help='print intermediate (untagged) layers'
    )
    parser.add_argument(
        '-f',
        '--format',
        dest='output_format',
        choices=('ascii', 'json'),
        default='ascii',
        help='the output format'
    )

    if 'argcomplete' in globals().keys():
        argcomplete.autocomplete(parser)

    return parser.parse_args(argv)


def main():
    """
    parse arguments and run the desired action
    """
    args = parse_args()

    layers = docktree.analyse_layers()
    if not args.print_intermediate:
        layers = docktree.remove_untagged_layers(layers)
    heads = docktree.get_heads(layers)
    print_tree(heads, output_format=args.output_format)

if __name__ == '__main__':
    main()