.PHONY: litellm

litellm:
	uv run --no-project --env-file .env litellm --config litellm-config.yml --port 4000
