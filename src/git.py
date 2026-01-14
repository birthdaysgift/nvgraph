import subprocess


def cmd(order_type, limit):
    cmd = f'git log --all --pretty=format:%h^%p^%D^%s^%an --max-count={limit} --{order_type}-order'
    result = subprocess.run(cmd.split(" "), cwd="/home/mint/code/ip_api_test_graph", capture_output=True)
    for line in result.stdout.strip().split(b"\n"):
        hash, parents = [v.decode() for v in line.split(b"^")][:2]
        yield hash, parents.split(" ")

