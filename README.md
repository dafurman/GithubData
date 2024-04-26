## Setup

1. Make `GITHUB_ACCESS_TOKEN` accessible in your environment.
2. `pip3 install ghapi`

# Commands

## Top Reviewers
This lets you figure out who's reviewed the most of a particular author's code, given a github owner and list of repos to examine.

```
./top_reviewers.py --repos <repo_a,repo_b,repo_c> <owner> <author>
```
