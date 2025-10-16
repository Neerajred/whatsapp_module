namespace WhatsAppModuleDotNet.Models;

/// <summary>
/// Represents a message template that can be sent to WhatsApp recipients.
/// </summary>
public class WhatsAppTemplate
{
    public int Id { get; set; }
    public required string Name { get; set; }
    public required string TemplateName { get; set; }
    public string Status { get; set; } = "PENDING";
    public required string Category { get; set; }
    public required string Language { get; set; }
    public required int AccountId { get; set; }
    public List<TemplateComponent> Components { get; set; } = new();
    public string? Body { get; set; }
    public string? HeaderMediaHandle { get; set; }
    public string? WhatsAppTemplateUid { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
