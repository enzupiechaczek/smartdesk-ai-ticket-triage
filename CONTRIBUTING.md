# How we work in this repository

## The golden rules

1. Never push to `main`. Everything goes through a pull request that Enzu reviews.
2. Work on your task branch. Branch names are listed in the Azure Boards task.
3. Sync with `main` before you push.
4. Commit small and often, with clear messages.
5. Synthetic data only. No secrets in code.

## Daily routine

Start of a session:

```
git checkout main
git pull origin main
git fetch origin
```

Move to your task branch and bring in teammates' work:

```
git checkout BRANCH-NAME
git pull origin BRANCH-NAME
git merge main
```

Work, then commit:

```
git status
git add path/to/file
git commit -m "Clear message in the present tense"
```

Before you push, sync with main:

```
git checkout main
git pull origin main
git checkout BRANCH-NAME
git pull origin BRANCH-NAME
git merge main
```

Push and open a pull request into `main`:

```
git push origin BRANCH-NAME
```

If Git says the push was rejected, a teammate pushed first. Run `git pull origin BRANCH-NAME` and push again.

## Sharing a task branch

Your group shares one branch per task. Agree who is typing. Always run `git pull origin BRANCH-NAME` before you start and before you push.

## Pull requests

- Open the pull request from your task branch into `main`.
- Fill in the pull request template.
- Enzu reviews. If changes are requested, fix them on the same branch and push again.
- After the merge, run `git checkout main` and `git pull origin main`.
- A merged branch is finished. Ask Enzu for a new branch if you need more changes.

## Merge conflicts

Open the file, choose which lines to keep, delete the `<<<<<<<`, `=======` and `>>>>>>>` lines, then run `git add FILE` and `git commit`. Run the app again to check it works. Ask for help if you are not sure.
