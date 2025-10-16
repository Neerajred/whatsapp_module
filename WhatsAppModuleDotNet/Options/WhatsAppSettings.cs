namespace WhatsAppModuleDotNet.Options;

public class WhatsAppSettings
{
    public int MinimumTokenLength { get; set; } = 10;

    public string DefaultTemplateCategory { get; set; } = "UTILITY";

    public string DefaultTemplateLanguage { get; set; } = "en_US";

    public string DefaultTemplateBody { get; set; } = "Hello {{1}}, welcome to our WhatsApp channel!";
}
