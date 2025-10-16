using Microsoft.AspNetCore.Mvc;

namespace WhatsAppModuleDotNet.Controllers;

[ApiController]
[Route("api/whatsapp/auth")]
public class AuthController : ControllerBase
{
    [HttpGet("generate-token")]
    public IActionResult GenerateToken()
    {
        var token = Convert.ToBase64String(Guid.NewGuid().ToByteArray());
        return Ok(new { access_token = token });
    }
}
