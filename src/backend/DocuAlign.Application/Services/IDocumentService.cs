namespace DocuAlign.Application.Services;

public interface IDocumentService
{
    Task<Guid> UploadDocumentAsync(Stream fileStream, string fileName, string contentType);
}