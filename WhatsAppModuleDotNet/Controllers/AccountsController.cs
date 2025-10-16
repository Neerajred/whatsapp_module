using Microsoft.AspNetCore.Mvc;
using WhatsAppModuleDotNet.Data;
using WhatsAppModuleDotNet.DTOs;
using WhatsAppModuleDotNet.Models;
using WhatsAppModuleDotNet.Services;

namespace WhatsAppModuleDotNet.Controllers;

[ApiController]
[Route("api/whatsapp/accounts")]
public class AccountsController : ControllerBase
{
    private readonly IWhatsAppRepository _repository;
    private readonly IWhatsAppApiService _service;

    public AccountsController(IWhatsAppRepository repository, IWhatsAppApiService service)
    {
        _repository = repository;
        _service = service;
    }

    [HttpGet]
    public IActionResult GetAccounts()
    {
        var accounts = _repository.GetAccounts();
        return Ok(new { success = true, data = accounts });
    }

    [HttpPost]
    public IActionResult CreateAccount([FromBody] CreateAccountRequest request)
    {
        var account = new WhatsAppAccount
        {
            Name = request.Name,
            AppUid = request.AppUid,
            AppSecret = request.AppSecret,
            AccountUid = request.AccountUid,
            PhoneUid = request.PhoneUid,
            Token = request.Token
        };

        account = _repository.AddAccount(account);
        return CreatedAtAction(nameof(GetAccounts), new { id = account.Id }, new { success = true, data = account });
    }

    [HttpPost("{accountId:int}/test")]
    public IActionResult TestAccountCredentials(int accountId)
    {
        var account = _repository.FindAccount(accountId);
        if (account is null)
        {
            return NotFound(new { error = "Account not found" });
        }

        try
        {
            _service.TestConnection(account);
            account.Status = "VALIDATED";
            return Ok(new { success = true, message = "Account credentials are valid." });
        }
        catch (WhatsAppApiException ex)
        {
            account.Status = "ERROR";
            return BadRequest(new { error = "Failed to validate account credentials.", details = ex.Message, code = ex.ErrorCode });
        }
    }

    [HttpPost("{accountId:int}/sync-templates")]
    public IActionResult SyncTemplates(int accountId)
    {
        var account = _repository.FindAccount(accountId);
        if (account is null)
        {
            return NotFound(new { error = "Account not found" });
        }

        try
        {
            var templates = _service.SyncTemplates(account);
            var results = new List<object>();
            foreach (var template in templates)
            {
                template.AccountId = account.Id;
                var savedTemplate = _repository.UpsertTemplate(template);
                results.Add(savedTemplate);
            }

            return Ok(new
            {
                success = true,
                message = "Templates synced successfully.",
                data = results
            });
        }
        catch (WhatsAppApiException ex)
        {
            return BadRequest(new { error = "Failed to sync templates due to an API error.", details = ex.Message, code = ex.ErrorCode });
        }
    }
}
