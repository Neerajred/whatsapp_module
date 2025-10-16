using System.ComponentModel.DataAnnotations;

namespace WhatsAppModuleDotNet.DTOs;

public class SendTemplateMessageRequest
{
    [Required]
    public int AccountId { get; set; }

    [Required]
    public string TemplateName { get; set; } = string.Empty;

    [Required]
    public string RecipientPhoneNumber { get; set; } = string.Empty;

    public List<string> BodyParams { get; set; } = new();
}
