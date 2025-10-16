using System.Linq;
using Microsoft.AspNetCore.Mvc;
using WhatsAppModuleDotNet.Data;
using WhatsAppModuleDotNet.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<IWhatsAppRepository, InMemoryWhatsAppRepository>();
builder.Services.AddSingleton<IWhatsAppApiService, FakeWhatsAppApiService>();
builder.Services.AddControllers().ConfigureApiBehaviorOptions(options =>
{
    options.InvalidModelStateResponseFactory = context =>
    {
        var errors = context.ModelState
            .Where(entry => entry.Value?.Errors.Any() == true)
            .Select(entry => new
            {
                Field = entry.Key,
                Messages = entry.Value!.Errors.Select(error => error.ErrorMessage).ToArray()
            });

        return new BadRequestObjectResult(new
        {
            Error = "ValidationError",
            Details = errors
        });
    };
});

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();

app.MapControllers();

app.Run();
