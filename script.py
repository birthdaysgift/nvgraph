import subprocess
import collections


def main():
    log = cmd()

    commits, tree = parse(log)
    for line in format(commits, tree):
        print(line)


def format(commits, tree):
    columns = []

    for commit in commits:
        children = tree[commit["hash"]]["children"]

        # ALGO BEGIN

        if len(children) == 0:
            commit["column"] = find_column(columns)
            yield get_line(commit)
            continue

        MC_children = [child for child in children if is_MC(child, tree)]
        RC_children = [child for child in children if is_RC(child, tree)]

        if MC_children:

            left_parent, right_parent = tree[MC_children[0]]["parents"]

            if commit["hash"] == right_parent:
                if RC_children:
                    commit["column"] = [commit for commit in commits if commit["hash"] == RC_children[0]][0]["column"]
                    yield get_line(commit)
                    continue
                if not RC_children:
                    commit["column"] = find_column(columns)
                    yield get_line(commit)
                    continue

            if commit["hash"] == left_parent:
                commit["column"] = [commit for commit in commits if commit["hash"] == MC_children[0]][0]["column"]

                if MC_children and RC_children:
                    for child in RC_children:
                        free_column(columns, [commit for commit in commits if commit["hash"] == child][0]["column"])

                yield get_line(commit)
                continue

        if RC_children:
            commit["column"] = [commit for commit in commits if commit["hash"] == RC_children[0]][0]["column"]
            yield get_line(commit)
            continue

        # ALGO END


def is_MC(hash, tree):
    return len(tree[hash]["parents"]) == 2


def is_RC(hash, tree):
    return not is_MC(hash, tree)


def get_line(commit):
    shift = (" | " * commit["column"])
    return f"{shift} * {commit['hash']}"


def find_column(columns):
    for column, occupied in enumerate(columns):
        if not occupied:
            columns[column] = True
            return column

    columns.append(True)
    return len(columns) - 1


def free_column(columns, column):
    columns[column] = False


def parse(text):
    commits = []
    tree = collections.defaultdict(lambda: {"parents": [], "children": []})

    for line in text.split(b"\n"):
        hash, parents, refs, subject, author = [v.decode() for v in line.split(b"^")]
        commits.append({"hash": hash, "refs": refs, "subject": subject, "author": author, "column": 0})

        for parent in parents.split(" "):
            tree[hash]["parents"].append(parent)
            tree[parent]["children"].append(hash)

    return commits, tree


def cmd():
    cmd = 'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count=50 --date-order'
    result = subprocess.run(cmd.split(" "), text=False, cwd="/home/mint/code/ip_api", capture_output=True)
    return result.stdout.strip()


if __name__ == "__main__":
    main()
