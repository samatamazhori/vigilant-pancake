#!/bin/bash

mkdir -p test_dotnet

projects=(
  "rpk.saja.cad.template.infra"
  "rpk.saja.cad.template.infra.db"
  "rpk.saja.cad.template.domain"
  "rpk.saja.cad.template.presentation"
)

for project in "${projects[@]}"
do
  mkdir -p "test_dotnet/${project}"
  touch "test_dotnet/${project}/${project}.csproj"

  dockerfile_content="FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY ${project}.csproj ./
RUN dotnet restore ${project}.csproj

# Copy everything else and build
COPY . .
RUN dotnet publish ${project}.csproj -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT [\"dotnet\", \"${project}.dll\"]"

  echo "$dockerfile_content" > "test_dotnet/${project}/Dockerfile"
done

touch "test_dotnet/rpk.saja.cad.template.sln"