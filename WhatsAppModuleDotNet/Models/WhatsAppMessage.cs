namespace WhatsAppModuleDotNet.Models;

/// <summary>
/// Represents a template message that was sent through WhatsApp.
/// </summary>
public class WhatsAppMessage
{
    public int Id { get; set; }
    public required int AccountId { get; set; }
    public required string TemplateName { get; set; }
    public required string RecipientPhoneNumber { get; set; }
    public List<string> BodyParameters { get; set; } = new();
    public DateTime SentAt { get; set; } = DateTime.UtcNow;
    public string Status { get; set; } = "SENT";
}
