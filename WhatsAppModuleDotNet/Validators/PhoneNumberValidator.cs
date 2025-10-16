using System.Text.RegularExpressions;

namespace WhatsAppModuleDotNet.Validators;

public static partial class PhoneNumberValidator
{
    [GeneratedRegex("^[0-9]{8,15}$")]
    private static partial Regex E164DigitsRegex();

    public static bool TryNormalize(string phoneNumber, out string? normalized)
    {
        var digitsOnly = new string(phoneNumber.Where(char.IsDigit).ToArray());
        if (!E164DigitsRegex().IsMatch(digitsOnly))
        {
            normalized = null;
            return false;
        }

        normalized = $"+{digitsOnly}";
        return true;
    }
}
