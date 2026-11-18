import { useEffect, useState } from "react";
import { FaUpload, FaTrash } from "react-icons/fa6";
import api from "../services/api";

function DocumentPanel({
  selectedDocument,
  setSelectedDocument,
}) {
  const [documents, setDocuments] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [stats, setStats] =
    useState({
      documents: 0,
      chunks: 0,
    });

  useEffect(() => {
    loadDocuments();
    loadStats();
  }, []);

  const loadDocuments =
    async () => {
      try {
        const res =
          await api.get(
            "/documents"
          );

        const docs =
          res.data.documents.map(
            (doc) => ({
              name: doc,
            })
          );

        setDocuments(docs);
      } catch (err) {
        console.log(
          "Documents Error:",
          err
        );
      }
    };

  const loadStats =
    async () => {
      try {
        const res =
          await api.get(
            "/stats"
          );

        setStats(
          res.data
        );
      } catch (err) {
        console.log(
          "Stats Error:",
          err
        );
      }
    };

  const uploadPdf =
    async (e) => {
      const file =
        e.target.files?.[0];

      if (!file) return;

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {
        setLoading(true);

        await api.post(
          "/upload-pdf",
          formData
        );

        await loadDocuments();
        await loadStats();
      } catch (err) {
        console.log(
          "Upload Error:",
          err
        );
      } finally {
        setLoading(false);

        e.target.value = "";
      }
    };

  const deleteDocument =
    async (docName) => {
      try {
        await api.delete(
          `/documents/${docName}`
        );

        await loadDocuments();
        await loadStats();

        if (
          selectedDocument ===
          docName
        ) {
          setSelectedDocument(
            "all"
          );
        }
      } catch (err) {
        console.log(
          "Delete Error:",
          err
        );
      }
    };

  return (
    <div className="sidebar">

      <h2 className="sidebar-title">
        Knowledge Base
      </h2>

      <div className="stats-card">

        <div className="stats-row">
          <span>
            Documents
          </span>

          <strong>
            {stats.documents}
          </strong>
        </div>

        <div className="stats-row">
          <span>
            Chunks
          </span>

          <strong>
            {stats.chunks}
          </strong>
        </div>

      </div>

      <label className="upload-btn">

        <FaUpload />

        <span>
          Upload PDF
        </span>

        <input
          type="file"
          accept=".pdf"
          hidden
          onChange={uploadPdf}
        />

      </label>

      {loading && (
        <p className="uploading">
          Uploading...
        </p>
      )}

      <div className="selector">

        <label>
          Search Scope
        </label>

        <select
          value={selectedDocument}
          onChange={(e) =>
            setSelectedDocument(
              e.target.value
            )
          }
        >

          <option value="all">
            All Documents
          </option>

          {documents.map(
            (doc) => (
              <option
                key={doc.name}
                value={doc.name}
              >
                {doc.name}
              </option>
            )
          )}

        </select>

      </div>

      <hr className="divider" />

      <div className="documents-section">

        <h3>
          Documents
        </h3>

        {documents.length ===
        0 ? (
          <div className="empty-state">
            No documents uploaded
            yet
          </div>
        ) : (
          <div className="document-list">

            {documents.map(
              (doc) => (
                <div
                  key={doc.name}
                  className="document-row"
                >

                  <div className="document-info">

                    <span className="doc-icon">
                      📄
                    </span>

                    <span
                      className="doc-name"
                      title={doc.name}
                    >
                      {doc.name}
                    </span>

                  </div>

                  <button
                    className="delete-btn"
                    onClick={() =>
                      deleteDocument(
                        doc.name
                      )
                    }
                  >
                    <FaTrash />
                  </button>

                </div>
              )
            )}

          </div>
        )}

      </div>

    </div>
  );
}

export default DocumentPanel;