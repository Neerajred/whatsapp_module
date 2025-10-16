# WhatsApp Module (.NET)

This repository now contains an ASP.NET Core 8.0 Web API that emulates key workflows of a WhatsApp Business integration. The service exposes endpoints for managing WhatsApp Business accounts, syncing templates, creating templates with media, and sending template-based messages.

## Getting started

1. Install the [.NET 8.0 SDK](https://dotnet.microsoft.com/download).
2. Restore dependencies and run the development server:

   ```bash
   dotnet restore WhatsAppModuleDotNet/WhatsAppModuleDotNet.csproj
   dotnet run --project WhatsAppModuleDotNet/WhatsAppModuleDotNet.csproj
   ```

3. Navigate to `https://localhost:5001/swagger` to explore and test the API surface.

The project uses an in-memory repository and a fake WhatsApp API service to keep the sample self-contained. Replace the implementations in `Data` and `Services` with real integrations when wiring up a production system.
