
# Pokemon Reverse Proxy Service
  

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

1.  **Python**: Version 3.9 or higher.

2.  **virtualenv**: For creating isolated Python environments.

3. **Git CLI**: For cloning the repository from GitHub.

## Installation and Usage
  

1. **Clone the repository**

	First, clone the project from GitHub:
	```bash
	git clone https://github.com/lidorkook/pokemon-proxy-service.git
	cd pokemon-proxy-service
	```

2.  **Run make all**

	The `Makefile` automates all necessary steps

	```bash
	make all
	```
	This command performs the following:

	-   Creates a virtual environment (`venv`) in the project directory.
	-   Installs all required dependencies from `requirements.txt`.
	-   Compiles the `.proto` files into Python classes.
	-   Starts the application.
## Notes
- The application re-triggers the stream initialization every 60 seconds as long as it is running.
- Ensure that your configuration file (`POKEPROXY_CONFIG`) is properly set in your `.env` file.
- The `.env` file is not included in the repository for security reasons. An example `.env` file is as follows:

	``` env
	IS_LOCAL=1 # so the application will know to connect to ngrok
	POKEPROXY_CONFIG=config.json # path to the pokemon configuration file
	STREAM_URL=https://hiring.external.guardio.dev # url of the stream service
	NGROK_AUTHTOKEN=2rzBfgMRdFCUGw8Zcx0mvc97eWd_5S5uxYxn8d9QvDuB8WNjj
	```
- In order to see the application's public url, look for the log `Ngrok tunnel started at` in the log files or `App URL:` in the terminal.