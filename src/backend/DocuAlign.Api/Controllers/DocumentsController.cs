using DocuAlign.Application.Common.Interfaces;
using DocuAlign.Application.Services;
using Microsoft.AspNetCore.Mvc;

namespace DocuAlign.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocumentsController : ControllerBase
{
    private readonly IDocumentService _documentService;
    private readonly IFileStorage _fileStorage;

    public DocumentsController(IDocumentService documentService,  IFileStorage fileStorage)
    {
        _documentService = documentService;
        _fileStorage = fileStorage;
    }

    [HttpPost("upload")]
    public async Task<IActionResult> Upload(IFormFile file)
    {
        if (file == null || file.Length == 0)
        {
            return BadRequest("No file uploaded.");
        }

        await using var stream = file.OpenReadStream();

        var documentId = await _documentService.UploadDocumentAsync(stream, file.FileName, file.ContentType);

        return Ok(new { DocumentId = documentId });
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetDocumentAsync(Guid id)
    {
        var document = await _documentService.GetDocumentAsync(id);
        if (document == null)
        {
            return NotFound("Document not found.");
        }

        var (fileBytes, _) = await _fileStorage.GetFileAsync(document.StoredPath);
        return File(fileBytes, document.ContentType, document.OriginalFileName);
    }
}