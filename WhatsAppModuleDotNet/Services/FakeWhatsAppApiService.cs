using System.Collections.Generic;
using System.Text.Json;
using Microsoft.Extensions.Options;
using WhatsAppModuleDotNet.Models;
using WhatsAppModuleDotNet.Options;

namespace WhatsAppModuleDotNet.Services;

/// <summary>
/// Fake implementation that emulates the Meta WhatsApp Business Platform interactions.
/// </summary>
public class FakeWhatsAppApiService : IWhatsAppApiService
{
    private readonly JsonSerializerOptions _serializerOptions = new(JsonSerializerDefaults.Web);
    private readonly WhatsAppSettings _settings;

    public FakeWhatsAppApiService(IOptions<WhatsAppSettings> options)
    {
        _settings = options.Value;
    }

    public void TestConnection(WhatsAppAccount account)
    {
        if (account.Token.Length < _settings.MinimumTokenLength)
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
            Category = _settings.DefaultTemplateCategory,
            Language = _settings.DefaultTemplateLanguage,
            Status = "APPROVED",
            Body = _settings.DefaultTemplateBody
        };

        template.Components.Add(new TemplateComponent
        {
            Type = "BODY",
            Parameters = new Dictionary<string, string[]>
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
                    parameters = component.Parameters.SelectMany(pair => pair.Value.Select(value => new { type = "text", text = value }))
                })
            }
        };

        _ = JsonSerializer.Serialize(payload, _serializerOptions);
        message.Status = "SENT";
        message.SentAt = DateTime.UtcNow;
        return message;
    }
}
