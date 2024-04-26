## Setup

1. Make `GITHUB_ACCESS_TOKEN` accessible in your environment.
2. `pip3 install ghapi`

# Commands

## Top Contributors
This prints a top 10 list of contributors, as well as a separate top 10 list of ["involved"](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-a-user-thats-involved-in-an-issue-or-pull-request) contributors, given a github owner and list of repos to examine.

```sh
./top_contributors.py --repos <repo_a,repo_b,repo_c> <owner>
```

## Top Reviewers
This prints a top 10 list of reviewers, given a github owner and list of repos to examine.

```sh
./top_reviewers.py --repos <repo_a,repo_b,repo_c> <owner>
```
