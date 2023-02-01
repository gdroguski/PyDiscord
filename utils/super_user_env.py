from parsing import ConfigParser, config_type


def run(config: config_type) -> None:
    """
    Creates environment variables for later migrations for superuser, if not given any then the
    default ones from the su.yaml will be set
    """
    with open(".env", "w") as env:
        env.write(f"DJANGO_SU_NAME={config.get('name')}\n")
        env.write(f"DJANGO_SU_EMAIL={config.get('email')}\n")
        env.write(f"DJANGO_SU_PASSWORD={config.get('password')}")


if __name__ == '__main__':
    current_config: config_type = ConfigParser("su.yaml").parse_args(log_changes=True)
    run(current_config)
