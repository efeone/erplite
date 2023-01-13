# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import functools
import math
import frappe
from frappe import _
from frappe.utils import add_days, add_months, cint, cstr, flt, formatdate, get_first_day, getdate
from six import itervalues

def filter_tasks(tasks, depth=20):
    parent_children_map = {}
    tasks_by_name = {}
    for d in tasks:
        tasks_by_name[d.name] = d
        parent_children_map.setdefault(d.parent_task or None, []).append(d)
    filtered_tasks = []

    def add_to_list(parent, level):
        if level < depth:
            children = parent_children_map.get(parent) or []
            for child in children:
                child.indent = level
                filtered_tasks.append(child)
                add_to_list(child.name, level + 1)
    add_to_list(None, 0)
    return filtered_tasks, tasks_by_name, parent_children_map
