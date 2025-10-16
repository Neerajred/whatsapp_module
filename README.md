# WhatsApp Module (.NET)

This repository now contains an ASP.NET Core 8.0 Web API that emulates key workflows of a WhatsApp Business integration. The service exposes endpoints for managing WhatsApp Business accounts, syncing templates, creating templates with media, and sending template-based messages.

## Getting started

1. Install the [.NET 8.0 SDK](https://dotnet.microsoft.com/download).
2. Restore dependencies and run the development server:

   ```bash
   dotnet restore WhatsAppModuleDotNet/WhatsAppModuleDotNet.csproj
   dotnet run --project WhatsAppModuleDotNet/WhatsAppModuleDotNet.csproj
   ```

3. Navigate to `https://localhost:5001/swagger` (or the HTTP port shown in the console output) to explore and test the API surface through Swagger UI. The UI now serves the `WhatsApp Module API v1` description from `/swagger/v1/swagger.json`.

The project uses an in-memory repository and a fake WhatsApp API service to keep the sample self-contained. Replace the implementations in `Data` and `Services` with real integrations when wiring up a production system.

## Configuration

Runtime settings are defined in `WhatsAppModuleDotNet/appsettings.json` and bound to the `WhatsAppSettings` options class. Adjust these values to fit your environment:

```json
{
  "WhatsApp": {
    "MinimumTokenLength": 10,
    "DefaultTemplateCategory": "UTILITY",
    "DefaultTemplateLanguage": "en_US",
    "DefaultTemplateBody": "Hello {{1}}, welcome to our WhatsApp channel!"
  }
}
```

> The app will use the defaults above if you do not override them via environment-specific appsettings files or other configuration providers supported by ASP.NET Core.
