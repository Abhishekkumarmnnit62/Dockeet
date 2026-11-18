from backend.core.dependencies import db

print(
    "Stored Chunks:",
    db.count()
)