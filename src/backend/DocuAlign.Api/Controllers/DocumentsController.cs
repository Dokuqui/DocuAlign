using DocuAlign.Application.Services;
using Microsoft.AspNetCore.Mvc;

namespace DocuAlign.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DocumentsController : ControllerBase
{
    private readonly IDocumentService _documentService;

    public DocumentsController(IDocumentService documentService)
    {
        _documentService = documentService;
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
}