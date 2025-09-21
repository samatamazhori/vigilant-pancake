FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY rpk.saja.cad.template.infra.csproj ./
RUN dotnet restore rpk.saja.cad.template.infra.csproj

# Copy everything else and build
COPY . .
RUN dotnet publish rpk.saja.cad.template.infra.csproj -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "rpk.saja.cad.template.infra.dll"]
