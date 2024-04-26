#!/usr/bin/env python3

from collections import defaultdict
from contributors import get_contributors
from ghapi.all import GhApi
import shared
import argparse
import time
import os

def print_top_involved(involved_counts_by_contributor: dict, repo: str = None):
    if repo is not None:
        print("Top 10 involved contributors since {} in the {} repo:".format(since, repo))
    else:
        print("Top 10 involved contributors since {}:".format(since))

    print("Rank\tContributor\tNumber of PRs involved")
    sorted_involved_counts = sorted(involved_counts_by_contributor.items(), key=lambda x: x[1], reverse=True)[:10]
    max_len_contributor = max(len(contributor) for contributor, _ in sorted_involved_counts)
    for i, (contributor, count) in enumerate(sorted_involved_counts, start=1):
        print(f"{i}\t{contributor.ljust(max_len_contributor)}\t{count}")
    print()

def print_top_contributors(contribution_counts_by_contributor: dict, repo: str = None):
    if repo is not None:
        print("Top 10 contributors since {} in the {} repo:".format(since, repo))
    else:
        print("Top 10 contributors since {}:".format(since))

    print("Rank\tContributor\tContribution Count")
    sorted_contribution_counts = sorted(contribution_counts_by_contributor.items(), key=lambda x: x[1], reverse=True)[:10]
    max_len_contributor = max(len(contributor) for contributor, _ in sorted_contribution_counts)
    for i, (contributor, count) in enumerate(sorted_contribution_counts, start=1):
        print(f"{i}\t{contributor.ljust(max_len_contributor)}\t{count}")
    print()

def get_involved_counts_by_contributor(contributors: list) -> dict:
    dict = {}
    for contributor_name in [c.login for c in contributors]:
        print(f"Getting involved counts for {contributor_name}")
        search_result = api.search.issues_and_pull_requests(
            q=f"repo:{owner}/{repo} is:merged involves:{contributor_name} -author:{contributor_name} created:>{since}"
        )
        dict[contributor_name] = search_result.total_count
        time.sleep(2) # Slow down to avoid rate limiting errors.
    return dict

def get_contribution_counts_by_contributor(contributors: list) -> dict:
    dict = {}
    for contributor_name in [c.login for c in contributors]:
        print(f"Getting contribution counts for {contributor_name}")
        search_result = api.search.issues_and_pull_requests(
            q=f"repo:{owner}/{repo} is:merged author:{contributor_name} created:>{since}"
        )
        dict[contributor_name] = search_result.total_count
        time.sleep(2) # Slow down to avoid rate limiting errors.
    return dict

parser = argparse.ArgumentParser(description="Get top contributors in an owner's repositories")
parser.add_argument("-m", "--min-contributions", type=int, help="the minimum number of contributions required")
parser.add_argument('--repos', type=shared.list_of_strings, help="The names of repositories")
parser.add_argument("owner", type=str, help="The owner of the repositories")
parser.add_argument("since", type=str, help="The start date to get information for")
args = parser.parse_args()

min_contributions = args.min_contributions
repos = args.repos
owner = args.owner
since = args.since
api = GhApi(token=os.getenv("GITHUB_ACCESS_TOKEN"))

total_countribution_counts_by_contributor = defaultdict(int)
total_involved_counts_by_contributor = defaultdict(int)

for repo in repos:
    print(f"Examining repo {repo}...")
    print("Getting contributors...")
    contributors = get_contributors(api=api, owner=owner, repo=repo, min_contributions=min_contributions)

    print("Getting contribution counts...")
    contribution_counts_by_contributor = get_contribution_counts_by_contributor(contributors=contributors)

    print("Getting involved counts...")
    involved_counts_by_contributor = get_involved_counts_by_contributor(contributors=contributors)

    total_countribution_counts_by_contributor = shared.merge_dicts(total_countribution_counts_by_contributor, contribution_counts_by_contributor)
    total_involved_counts_by_contributor = shared.merge_dicts(total_involved_counts_by_contributor, involved_counts_by_contributor)

    print_top_contributors(contribution_counts_by_contributor=contribution_counts_by_contributor, repo=repo)
    print_top_involved(involved_counts_by_contributor=involved_counts_by_contributor, repo=repo)

print_top_contributors(contribution_counts_by_contributor=total_countribution_counts_by_contributor)
print_top_involved(involved_counts_by_contributor=total_involved_counts_by_contributor)
