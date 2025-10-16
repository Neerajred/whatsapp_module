namespace WhatsAppModuleDotNet.Models;

/// <summary>
/// Describes a template component as expected by the WhatsApp Business API.
/// </summary>
public class TemplateComponent
{
    public required string Type { get; set; }
    public Dictionary<string, object> Parameters { get; set; } = new();
    public Dictionary<string, object>? Example { get; set; }
}
