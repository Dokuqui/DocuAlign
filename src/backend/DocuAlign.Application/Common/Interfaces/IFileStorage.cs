namespace DocuAlign.Application.Common.Interfaces;

public interface IFileStorage
{
    Task<string>SaveFileAsync(Stream fileStream, string fileName, string contentType);
}