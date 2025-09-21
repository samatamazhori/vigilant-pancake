#!/bin/bash
rm -rf test_dotnet
rm -rf test_repo
bash make_test.sh
echo "Clean slate."
python3 orch.py
docker buildx build -f test_repo/Dockerfile.develop test_repo/ 