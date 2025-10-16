using System.ComponentModel.DataAnnotations;

namespace WhatsAppModuleDotNet.DTOs;

public class CreateAccountRequest
{
    [Required]
    public string Name { get; set; } = string.Empty;

    [Required]
    public string AppUid { get; set; } = string.Empty;

    [Required]
    public string AppSecret { get; set; } = string.Empty;

    [Required]
    public string AccountUid { get; set; } = string.Empty;

    [Required]
    public string PhoneUid { get; set; } = string.Empty;

    [Required]
    public string Token { get; set; } = string.Empty;
}
