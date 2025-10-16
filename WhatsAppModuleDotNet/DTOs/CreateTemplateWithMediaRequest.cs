using System.ComponentModel.DataAnnotations;
using WhatsAppModuleDotNet.Models;

namespace WhatsAppModuleDotNet.DTOs;

public class CreateTemplateWithMediaRequest
{
    [Required]
    public string Name { get; set; } = string.Empty;

    [Required]
    public string Language { get; set; } = string.Empty;

    [Required]
    public string Category { get; set; } = string.Empty;

    [Required]
    public int AccountId { get; set; }

    [MinLength(1)]
    public List<TemplateComponent> Components { get; set; } = new();
}
