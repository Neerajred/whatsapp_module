using System.Collections.Concurrent;
using WhatsAppModuleDotNet.Models;

namespace WhatsAppModuleDotNet.Data;

/// <summary>
/// Simple in-memory repository that emulates persistence for demo purposes.
/// </summary>
public class InMemoryWhatsAppRepository : IWhatsAppRepository
{
    private readonly ConcurrentDictionary<int, WhatsAppAccount> _accounts = new();
    private readonly ConcurrentDictionary<(int AccountId, string TemplateName), WhatsAppTemplate> _templates = new();
    private readonly ConcurrentDictionary<int, WhatsAppMessage> _messages = new();
    private int _accountIdSequence;
    private int _templateIdSequence;
    private int _messageIdSequence;

    public IReadOnlyCollection<WhatsAppAccount> GetAccounts() => _accounts.Values.OrderBy(account => account.Id).ToArray();

    public WhatsAppAccount AddAccount(WhatsAppAccount account)
    {
        account.Id = Interlocked.Increment(ref _accountIdSequence);
        _accounts[account.Id] = account;
        return account;
    }

    public WhatsAppAccount? FindAccount(int accountId)
    {
        _accounts.TryGetValue(accountId, out var account);
        return account;
    }

    public WhatsAppTemplate UpsertTemplate(WhatsAppTemplate template)
    {
        if (template.Id == 0)
        {
            template.Id = Interlocked.Increment(ref _templateIdSequence);
        }

        var key = (template.AccountId, template.TemplateName.ToLowerInvariant());
        _templates[key] = template;
        return template;
    }

    public WhatsAppTemplate? FindTemplate(int accountId, string templateName)
    {
        var key = (accountId, templateName.ToLowerInvariant());
        _templates.TryGetValue(key, out var template);
        return template;
    }

    public IReadOnlyCollection<WhatsAppTemplate> GetTemplates(int accountId)
    {
        return _templates
            .Where(pair => pair.Key.AccountId == accountId)
            .Select(pair => pair.Value)
            .OrderBy(template => template.Id)
            .ToArray();
    }

    public WhatsAppMessage AddMessage(WhatsAppMessage message)
    {
        message.Id = Interlocked.Increment(ref _messageIdSequence);
        _messages[message.Id] = message;
        return message;
    }
}
