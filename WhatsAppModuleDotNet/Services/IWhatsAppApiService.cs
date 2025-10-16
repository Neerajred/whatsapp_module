using WhatsAppModuleDotNet.Models;

namespace WhatsAppModuleDotNet.Services;

public interface IWhatsAppApiService
{
    void TestConnection(WhatsAppAccount account);
    IReadOnlyCollection<WhatsAppTemplate> SyncTemplates(WhatsAppAccount account);
    string UploadMedia(Stream stream, string fileName);
    WhatsAppTemplate CreateTemplate(WhatsAppAccount account, WhatsAppTemplate template);
    WhatsAppMessage SendTemplateMessage(WhatsAppAccount account, WhatsAppTemplate template, WhatsAppMessage message);
}
