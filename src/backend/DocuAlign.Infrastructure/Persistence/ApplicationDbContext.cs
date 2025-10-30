using DocuAlign.Application.Common.Interfaces;
using DocuAlign.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace DocuAlign.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) {}
    
    public DbSet<Document> Documents => Set<Document>();
}