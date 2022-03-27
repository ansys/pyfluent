import subprocess


def stop_fluent_container():
    subprocess.run(["docker", "stop", "fluent_server"])


if __name__ == "__main__":
    stop_fluent_container()
