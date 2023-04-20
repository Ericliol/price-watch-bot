# Contributing to the Price Watch Project

## How to contribute

### Create your branch

``` bash
git checkout -b <branch_name>
```

Branch name could be `fix-XXXX` if you are fixing something, or `feature-YYYY` if you are adding a new feature

### Check your changes

Before commiting your code, make sure you checked if all changes are required by

```bash
git diff
```

### Commit your changes

Commit your branch by

``` bash
git add .
git commit -m "<commit_message>"
```

Commit message need to include:

- What you are fixing
- Why are you fixing

### Push your changes

Push your changes by

``` bash
git push
```

### Create a pull request

Log in to github, and create a pull request
Add relavent team member as reviewers
Wait for reviewer to approve your PR

Once your PR is approved.

### Rebase your branch

Rebase your branch by

``` bash
git rebase origin/master
```

Fix the conflicts if any, and then do:

``` bash
git push -f
```

Wait for unit-testing to pass, and then Click 'Merge button on your pull request
