import uvicorn
from src.settings import AUTO_RELOAD


def main() -> None:
    uvicorn.run(
        app="src.app:app",
        host="0.0.0.0",
        port=8080,
        reload=AUTO_RELOAD,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
