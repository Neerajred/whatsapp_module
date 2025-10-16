namespace WhatsAppModuleDotNet.Services;

public class WhatsAppApiException : Exception
{
    public string ErrorCode { get; }

    public WhatsAppApiException(string errorCode, string message) : base(message)
    {
        ErrorCode = errorCode;
    }
}
