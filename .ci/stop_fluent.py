import subprocess


def stop_fluent_container():
    try:
        subprocess.run(["docker", "stop", "fluent_server"])
    except OSError:
        pass


if __name__ == "__main__":
    stop_fluent_container()
