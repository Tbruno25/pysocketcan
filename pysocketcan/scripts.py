from subprocess import check_output


def run_script(script):
    """
    Execute script directly in linux environment.
    """

    def run(script):
        return check_output(script, shell=True).decode("utf8").strip()

    def wrapper(*args, **kwargs):
        return run(script(*args, **kwargs))

    return wrapper if callable(script) else run(script)


@run_script
def get(id, start, end=""):
    script = f"ip -d link show {id}"
    parse = f"grep -oP '(?<={start}).*(?={end})'"
    return f"{script} | {parse}" if start else script


def get_states(id):
    return get(id, "state", "restart-ms")


def get_modes(id):
    return get(id, "can <", "> state")


def get_baud(id):
    return get(id, "bitrate", "sample-point")


@run_script
def get_interfaces():
    return "ls /sys/class/net | grep can"


@run_script
def set(id, args_1="type can", args_2=""):
    return f"ip link set {id} {args_1} {args_2}"


def set_baud(id, rate):
    set(id, args_2=f"bitrate {rate}")


@run_script
def send(id, can_id, data):
    """Hint: Use underscores to seperate bytes 12_34_56_78"""
    return f"cansend {id} {can_id}#{data}"


@run_script
def candump(id, args="-n 1"):
    return f"candump {args} {id}"
