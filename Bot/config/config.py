import yaml


with open("Bot/bot_config.yml", "r") as f:
    config = yaml.safe_load(f)

    DEFAULT_CONFIG = config["DEFAULT_CONFIG"]
    COGS = config["COGS"]
    DATABASE = config["DATABASE"]
    is_in_development_mode = config['is_in_development_mode']
