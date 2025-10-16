using WhatsAppModuleDotNet.Models;

namespace WhatsAppModuleDotNet.Data;

public interface IWhatsAppRepository
{
    IReadOnlyCollection<WhatsAppAccount> GetAccounts();
    WhatsAppAccount AddAccount(WhatsAppAccount account);
    WhatsAppAccount? FindAccount(int accountId);
    WhatsAppTemplate UpsertTemplate(WhatsAppTemplate template);
    WhatsAppTemplate? FindTemplate(int accountId, string templateName);
    IReadOnlyCollection<WhatsAppTemplate> GetTemplates(int accountId);
    WhatsAppMessage AddMessage(WhatsAppMessage message);
}
