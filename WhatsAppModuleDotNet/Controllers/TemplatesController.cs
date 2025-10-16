using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using WhatsAppModuleDotNet.Data;
using WhatsAppModuleDotNet.DTOs;
using WhatsAppModuleDotNet.Models;
using WhatsAppModuleDotNet.Services;

namespace WhatsAppModuleDotNet.Controllers;

[ApiController]
[Route("api/whatsapp/templates")]
public class TemplatesController : ControllerBase
{
    private readonly IWhatsAppRepository _repository;
    private readonly IWhatsAppApiService _service;
    private readonly JsonSerializerOptions _serializerOptions = new(JsonSerializerDefaults.Web);

    public TemplatesController(IWhatsAppRepository repository, IWhatsAppApiService service)
    {
        _repository = repository;
        _service = service;
    }

    [HttpPost("create-with-media")]
    [Consumes("multipart/form-data")]
    public async Task<IActionResult> CreateTemplateWithMedia([FromForm(Name = "template_data")] string templateData, [FromForm(Name = "file")] IFormFile file)
    {
        if (string.IsNullOrWhiteSpace(templateData) || file is null)
        {
            return BadRequest(new { error = "Request must include 'template_data' and 'file' parts." });
        }

        CreateTemplateWithMediaRequest? request;
        try
        {
            request = JsonSerializer.Deserialize<CreateTemplateWithMediaRequest>(templateData, _serializerOptions);
        }
        catch (JsonException ex)
        {
            return BadRequest(new { error = "'template_data' must be a valid JSON string.", details = ex.Message });
        }

        if (request is null)
        {
            return BadRequest(new { error = "Template data could not be parsed." });
        }

        if (!TryValidateModel(request))
        {
            return ValidationProblem(ModelState);
        }

        if (file.Length == 0)
        {
            return BadRequest(new { error = "A valid file must be provided." });
        }

        var account = _repository.FindAccount(request.AccountId);
        if (account is null || !string.Equals(account.Status, "VALIDATED", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { error = "A valid, validated account is required." });
        }

        var headerComponent = request.Components.FirstOrDefault(component => string.Equals(component.Type, "HEADER", StringComparison.OrdinalIgnoreCase));
        if (headerComponent is null)
        {
            return BadRequest(new { error = "Template data must include a 'HEADER' component for media." });
        }

        try
        {
            await using var memoryStream = new MemoryStream();
            await file.CopyToAsync(memoryStream);
            memoryStream.Position = 0;
            var mediaHandle = _service.UploadMedia(memoryStream, file.FileName);

            headerComponent.Example = new Dictionary<string, object>
            {
                ["header_handle"] = new[] { mediaHandle }
            };

            var template = new WhatsAppTemplate
            {
                Name = request.Name,
                TemplateName = request.Name,
                Language = request.Language,
                Category = request.Category,
                AccountId = request.AccountId,
                Components = request.Components,
                HeaderMediaHandle = mediaHandle
            };

            template = _service.CreateTemplate(account, template);
            template = _repository.UpsertTemplate(template);

            return CreatedAtAction(nameof(CreateTemplateWithMedia), new { id = template.Id }, new
            {
                success = true,
                message = "Template with media submitted and permanent handle saved.",
                data = template
            });
        }
        catch (WhatsAppApiException ex)
        {
            return BadRequest(new { error = "Failed to process template with media.", details = ex.Message, code = ex.ErrorCode });
        }
    }
}
