#!/usr/bin/env python3

from ghapi.all import GhApi

def get_contributors(api: GhApi, owner: str, repo: str, min_contributions: int) -> list:
    contributors = api.repos.list_contributors(owner=owner, repo=repo)
    if min_contributions is not None:
        contributors = [c for c in contributors if c.contributions > min_contributions]
    else:
        contributors = [c for c in contributors]
    
    contributors = list(filter(lambda contributors: contributors.type == "User", contributors))
    return contributors
