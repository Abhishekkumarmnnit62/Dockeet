from backend.core.dependencies import (
    db,
    chunk_store
)
from pydantic import BaseModel
from fastapi.middleware.cors import (
    CORSMiddleware
)
from backend.metrics.metrics_service import (
    metrics_service
)



from backend.services.query_service import QueryService
from fastapi import (
    FastAPI,
    UploadFile,
    File
)
from backend.services.ingestion_service import (
    IngestionService
)


app = FastAPI(
    title="Production RAG API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = QueryService()
ingestor = IngestionService()


class QuestionRequest(BaseModel):
    question: str
    document_name: str


@app.get("/")
def home():

    return {
        "status": "running",
        "message": "Production RAG API is live"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag.ask(
        request.question,
        request.document_name
    )

    return {
        "question": request.question,
        "document_name": request.document_name,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = (
        f"data/raw_docs/{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    result = (
        ingestor.ingest_pdf(
            file_path
        )
    )

    return result


@app.get("/documents")
def list_documents():

    documents = (
        chunk_store.list_documents()
    )

    return {
        "total_documents":
        len(documents),

        "documents":
        documents
    }


@app.delete(
    "/documents/{document_name}"
)
def delete_document(
    document_name: str
):

    deleted = (
        db.delete_document(
            document_name
        )
    )

    chunk_store.delete_document(
         document_name
    )

    return {
        "document":
        document_name,

        "deleted_chunks":
        deleted
    }


@app.get("/stats")
def get_stats():

    return {
        "documents":
        chunk_store.get_document_count(),

        "chunks":
        chunk_store.count()
    }

class DebugRequest(
    BaseModel
):
    question: str
    document_name: str

from backend.services.debug_service import (
    DebugService
)

debug_service = (
    DebugService()
)


@app.post(
    "/debug-retrieval"
)
def debug_retrieval(
    request: DebugRequest
):

    return debug_service.debug(
        request.question,
        request.document_name
    )


@app.get("/metrics")
def get_metrics():

    return (
        metrics_service
        .get_metrics()
    )

@app.delete("/metrics/reset")
def reset_metrics():

    metrics_service.reset()

    return {
        "message":
        "Metrics reset successfully"
    }