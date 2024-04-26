## Setup

1. Make `GITHUB_ACCESS_TOKEN` accessible in your environment.
2. `pip3 install ghapi`

# Commands

## Top Reviewers
This prints a top 10 list of reviewers, given a github owner and list of repos to examine.

```sh
./top_reviewers.py --repos <repo_a,repo_b,repo_c> <owner>
```
