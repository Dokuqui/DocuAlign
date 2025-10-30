using DocuAlign.Application.Common.Interfaces;

namespace DocuAlign.Infrastructure.Services;

public class FileSystemStorage : IFileStorage
{
    private readonly string _uploadPath;
    
    public FileSystemStorage()
    {
        _uploadPath = Path.Combine(Directory.GetCurrentDirectory(), "Uploads");
        if (!Directory.Exists(_uploadPath))
        {
            Directory.CreateDirectory(_uploadPath);
        }
    }

    public async Task<string> SaveFileAsync(Stream fileStream, string fileName, string contentType)
    {
        var filePath = Path.Combine(_uploadPath, fileName);

        await using var stream = new FileStream(filePath, FileMode.Create);
        await fileStream.CopyToAsync(stream);
        
        return fileName;
    }

    public async Task<(byte[] FileBytes, string ContentType)> GetFileAsync(string storedPath)
    {
        var filePath = Path.Combine(_uploadPath, storedPath);

        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException("File not found.", storedPath);
        }
        
        var fileBytes = await File.ReadAllBytesAsync(filePath);
        return (fileBytes, string.Empty);
    }
}