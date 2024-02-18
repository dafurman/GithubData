#!/usr/bin/env python3

def merge_dicts(dict1: dict, dict2: dict):
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict:
            merged_dict[key] += value
        else:
            merged_dict[key] = value
    return merged_dict

def list_of_strings(arg: str):
    return arg.split(',')
