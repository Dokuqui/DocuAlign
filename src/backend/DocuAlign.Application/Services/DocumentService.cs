using DocuAlign.Application.Common.Interfaces;
using DocuAlign.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace DocuAlign.Application.Services;

public class DocumentService : IDocumentService
{
    private readonly IApplicationDbContext _context;
    private readonly IFileStorage _fileStorage;

    public DocumentService(IApplicationDbContext context, IFileStorage fileStorage)
    {
        _context = context;
        _fileStorage = fileStorage;
    }

    public async Task<Guid> UploadDocumentAsync(Stream fileStream, string fileName, string contentType)
    {
        var fileExtension = Path.GetExtension(fileName);
        var uniqueFileName = $"{Guid.NewGuid()}{fileExtension}";
        var storedPath = await _fileStorage.SaveFileAsync(fileStream, uniqueFileName, contentType);

        var document = new Document
        {
            Id = Guid.NewGuid(),
            OriginalFileName = fileName,
            StoredPath = storedPath,
            ContentType = contentType,
            UploadedAt = DateTime.UtcNow
        };

        await _context.Documents.AddAsync(document);
        await _context.SaveChangesAsync(CancellationToken.None);

        return document.Id;
    }

    public async Task<Document?> GetDocumentAsync(Guid id)
    {
        return await _context.Documents.FirstOrDefaultAsync(d => d.Id == id);
    }
}