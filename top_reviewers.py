#!/usr/bin/env python3

from collections import defaultdict
from contributors import get_contributors
from ghapi.all import GhApi
import shared
import argparse
import time
import os

def print_top_reviewers(review_counts_by_reviewer: dict, repo: str = None):
    if repo is not None:
        print("Top 10 reviewers of {}'s code since {} in the {} repo:".format(author, since, repo))
    else:
        print("Top 10 reviewers of {}'s code since {}:".format(author, since))

    print("Rank\tReviewer\tReview Count")
    sorted_review_counts = sorted(review_counts_by_reviewer.items(), key=lambda x: x[1], reverse=True)[:10]
    max_len_reviewer = max(len(reviewer) for reviewer, _ in sorted_review_counts)
    for i, (reviewer, count) in enumerate(sorted_review_counts, start=1):
        print(f"{i}\t{reviewer.ljust(max_len_reviewer)}\t{count}")
    print()

def get_review_counts_by_reviewer(contributors: list) -> dict:
    dict = {}
    for reviewer_name in [c.login for c in contributors]:
        print(f"Getting review counts for {reviewer_name}")
        if reviewer_name == author:
            continue

        search_result = api.search.issues_and_pull_requests(
            q=f"repo:{owner}/{repo} is:merged author:{author} reviewed-by:{reviewer_name} created:>{since}"
        )
        dict[reviewer_name] = search_result.total_count
        time.sleep(2) # Slow down to avoid rate limiting errors.
    return dict

parser = argparse.ArgumentParser(description="Get top reviewers for a given code author in an owner's repositories")
parser.add_argument("-m", "--min-contributions", type=int, help="the minimum number of contributions required")
parser.add_argument('--repos', type=shared.list_of_strings, help="The names of repositories")
parser.add_argument("owner", type=str, help="The owner of the repositories")
parser.add_argument("author", type=str, help="The person to inspect reviews for")
parser.add_argument("since", type=str, help="The start date to get information for")
args = parser.parse_args()

min_contributions = args.min_contributions
repos = args.repos
owner = args.owner
author = args.author
since = args.since
api = GhApi(token=os.getenv("GITHUB_ACCESS_TOKEN"))

total_review_counts_by_reviewer = defaultdict(int)

for repo in repos:
    print(f"Examining repo {repo}...")
    print("Getting contributors...")
    contributors = get_contributors(api=api, owner=owner, repo=repo, min_contributions=min_contributions)
    print("Getting review counts...")
    review_counts_by_reviewer = get_review_counts_by_reviewer(contributors=contributors)
    total_review_counts_by_reviewer = shared.merge_dicts(total_review_counts_by_reviewer, review_counts_by_reviewer)
    print_top_reviewers(review_counts_by_reviewer=review_counts_by_reviewer, repo=repo)

print_top_reviewers(review_counts_by_reviewer=total_review_counts_by_reviewer)
