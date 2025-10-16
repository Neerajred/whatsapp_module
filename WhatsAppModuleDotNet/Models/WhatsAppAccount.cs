namespace WhatsAppModuleDotNet.Models;

/// <summary>
/// Represents credentials and metadata required to interact with Meta's WhatsApp Business API.
/// </summary>
public class WhatsAppAccount
{
    public int Id { get; set; }
    public required string Name { get; set; }
    public required string AppUid { get; set; }
    public required string AppSecret { get; set; }
    public required string AccountUid { get; set; }
    public required string PhoneUid { get; set; }
    public required string Token { get; set; }
    public string Status { get; set; } = "PENDING";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
