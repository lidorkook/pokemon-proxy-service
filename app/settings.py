from environs import Env

env = Env()
env.read_env(override=True)

IS_LOCAL = env.bool("IS_LOCAL")
POKEPROXY_CONFIG = env.str("POKEPROXY_CONFIG")
STREAM_URL = env.str("STREAM_URL")
NGROK_AUTHTOKEN = env.str("NGROK_AUTHTOKEN")
PROXY_SERVICE_URL = env.str("PROXY_SERVICE_URL", "")
PORT = env.int("PORT", 5001)
