using Microsoft.AspNetCore.Mvc;
using WhatsAppModuleDotNet.Data;
using WhatsAppModuleDotNet.DTOs;
using WhatsAppModuleDotNet.Models;
using WhatsAppModuleDotNet.Services;
using WhatsAppModuleDotNet.Validators;

namespace WhatsAppModuleDotNet.Controllers;

[ApiController]
[Route("api/whatsapp/messages")]
public class MessagesController : ControllerBase
{
    private readonly IWhatsAppRepository _repository;
    private readonly IWhatsAppApiService _service;

    public MessagesController(IWhatsAppRepository repository, IWhatsAppApiService service)
    {
        _repository = repository;
        _service = service;
    }

    [HttpPost("send-template")]
    public IActionResult SendTemplate([FromBody] SendTemplateMessageRequest request)
    {
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var account = _repository.FindAccount(request.AccountId);
        if (account is null || !string.Equals(account.Status, "VALIDATED", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { error = "A valid, validated account is required." });
        }

        var template = _repository.FindTemplate(request.AccountId, request.TemplateName);
        if (template is null || !string.Equals(template.Status, "APPROVED", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { error = "A valid, approved template is required." });
        }

        if (!PhoneNumberValidator.TryNormalize(request.RecipientPhoneNumber, out var normalizedNumber))
        {
            return BadRequest(new { error = "Invalid recipient phone number." });
        }

        var message = new WhatsAppMessage
        {
            AccountId = request.AccountId,
            TemplateName = request.TemplateName,
            RecipientPhoneNumber = normalizedNumber!,
            BodyParameters = request.BodyParams ?? new List<string>()
        };

        try
        {
            message = _service.SendTemplateMessage(account, template, message);
            message = _repository.AddMessage(message);
            return Ok(new { success = true, message = "Template message delivered.", data = message });
        }
        catch (WhatsAppApiException ex)
        {
            return BadRequest(new { error = "Failed to send template message.", details = ex.Message, code = ex.ErrorCode });
        }
    }
}
