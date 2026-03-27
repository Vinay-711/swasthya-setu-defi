from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_modules.document_ai import processor
from app.ai_modules.bhashasehat import translate_text
from app.core.config import settings
from app.models.document import Document
from database.mongo import mongo_db


class DocumentService:
    def __init__(self) -> None:
        self.storage_path = Path(settings.storage_dir) / "documents"
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def create_document(
        self,
        db: AsyncSession,
        worker_id: str,
        file_name: str,
        file_bytes: bytes,
    ) -> Document:
        safe_name = file_name.replace("/", "_")
        persisted_name = f"{worker_id}-{safe_name}"
        output_path = self.storage_path / persisted_name
        output_path.write_bytes(file_bytes)

        parsed_json = processor.process(file_bytes, file_name)

        row = Document(
            worker_id=worker_id,
            original_path=str(output_path),
            parsed_json=parsed_json,
            status="processed",
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)

        # Mirror unstructured document payload in MongoDB for analytics workflows.
        if mongo_db is not None:
            await mongo_db["documents"].insert_one(
                {
                    "document_id": row.id,
                    "worker_id": worker_id,
                    "raw": json.dumps(parsed_json),
                }
            )

        return row

    async def get_document(self, db: AsyncSession, document_id: str) -> Document | None:
        return await db.get(Document, document_id)

    async def list_documents_by_worker(self, db: AsyncSession, worker_id: str) -> list[Document]:
        result = await db.execute(
            select(Document).where(Document.worker_id == worker_id).order_by(desc(Document.created_at))
        )
        return list(result.scalars().all())

    async def translate_document(self, db: AsyncSession, doc: Document, target_language: str) -> Document:
        raw_text = str(doc.parsed_json.get("raw_text", ""))
        translated = translate_text(text=raw_text, source_language="en", target_language=target_language)

        parsed_json = dict(doc.parsed_json)
        parsed_json["translated_text"] = translated
        parsed_json["target_language"] = target_language
        doc.parsed_json = parsed_json
        await db.commit()
        await db.refresh(doc)
        return doc


document_service = DocumentService()
