.PHONY: litellm

litellm:
	uv run --no-project --env-file .env litellm --config config.yaml --port 4000
