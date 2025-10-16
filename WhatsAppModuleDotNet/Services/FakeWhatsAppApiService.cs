using System.Text.Json;
using WhatsAppModuleDotNet.Models;

namespace WhatsAppModuleDotNet.Services;

/// <summary>
/// Fake implementation that emulates the Meta WhatsApp Business Platform interactions.
/// </summary>
public class FakeWhatsAppApiService : IWhatsAppApiService
{
    private readonly JsonSerializerOptions _serializerOptions = new(JsonSerializerDefaults.Web);

    public void TestConnection(WhatsAppAccount account)
    {
        if (account.Token.Length < 10)
        {
            throw new WhatsAppApiException("TokenTooShort", "The provided access token is too short to be realistic.");
        }
    }

    public IReadOnlyCollection<WhatsAppTemplate> SyncTemplates(WhatsAppAccount account)
    {
        var template = new WhatsAppTemplate
        {
            Name = $"welcome_{account.Id}",
            TemplateName = $"welcome_{account.Id}",
            AccountId = account.Id,
            Category = "UTILITY",
            Language = "en_US",
            Status = "APPROVED",
            Body = "Hello {{1}}, welcome to our WhatsApp channel!"
        };

        template.Components.Add(new TemplateComponent
        {
            Type = "BODY",
            Parameters =
            {
                ["example"] = new[] { "friend" }
            }
        });

        return new[] { template };
    }

    public string UploadMedia(Stream stream, string fileName)
    {
        if (stream.Length == 0)
        {
            throw new WhatsAppApiException("EmptyFile", "Uploaded media cannot be empty.");
        }

        return $"media_{Guid.NewGuid():N}";
    }

    public WhatsAppTemplate CreateTemplate(WhatsAppAccount account, WhatsAppTemplate template)
    {
        template.Status = "PENDING";
        template.WhatsAppTemplateUid = $"tmpl_{Guid.NewGuid():N}";
        return template;
    }

    public WhatsAppMessage SendTemplateMessage(WhatsAppAccount account, WhatsAppTemplate template, WhatsAppMessage message)
    {
        var payload = new
        {
            messaging_product = "whatsapp",
            to = message.RecipientPhoneNumber,
            type = "template",
            template = new
            {
                name = template.TemplateName,
                language = new { code = template.Language.ToLowerInvariant() },
                components = template.Components.Select(component => new
                {
                    type = component.Type.ToLowerInvariant(),
                    parameters = component.Parameters.Select(pair => new { type = "text", text = pair.Value.ToString() })
                })
            }
        };

        _ = JsonSerializer.Serialize(payload, _serializerOptions);
        message.Status = "SENT";
        message.SentAt = DateTime.UtcNow;
        return message;
    }
}
