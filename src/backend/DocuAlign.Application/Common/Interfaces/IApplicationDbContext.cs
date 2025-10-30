using DocuAlign.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace DocuAlign.Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<Document> Documents { get; }

    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
}