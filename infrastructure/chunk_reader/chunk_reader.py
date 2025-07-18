import os

import faiss
from docx import Document
from sentence_transformers import SentenceTransformer
from sqlalchemy import Integer, Text, create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from infrastructure.database.ORMmodels import Base
import numpy


def read_chunks_from_file():
    doc = Document('chunks.docx')
    chunk_list = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            chunk_list.append(text)
    return chunk_list


def get_vectors_from_chunks(chunk_list):
    vectors = []
    model = SentenceTransformer('models/all-MiniLM-L6-v2')
    for chunk in chunk_list:
        embedding = model.encode(chunk, convert_to_numpy=True)
        vectors.append(embedding)
    vectors = numpy.array(vectors)
    vectors = vectors / numpy.linalg.norm(vectors, axis=1, keepdims=True)  # 🔧 нормализация
    return vectors


class AIChunk(Base):
    __tablename__ = 'chunks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chunk_text: Mapped[str] = mapped_column(Text)


def write_chunks_to_db(session, chunk_list):
    chunk_objects = []
    for chunk in chunk_list:
        obj = AIChunk(chunk_text=chunk)
        chunk_objects.append(obj)
    session.add_all(chunk_objects)
    session.commit()   # атрибуты объектов AIChunk обновляются в коде. Работает в пределах сессии.
    ids = [obj.id for obj in chunk_objects]
    return ids


def create_faiss_index(dimension, filename='faiss.index'):
    base_index = faiss.IndexFlatIP(dimension)  # 🔁 был L2, стал IP (inner product, для косинусного сходства)
    index = faiss.IndexIDMap(base_index)  # оборачиваем, чтобы можно было добавлять id
    faiss.write_index(index, filename)  # сохраняем пустой индекс в файл


def add_vectors_to_faiss(vectors, ids, path):
    index = faiss.read_index(path)                    # загружаем индекс из файла
    vectors_np = numpy.array(vectors).astype('float32')  # приводим список векторов к numpy массиву
    ids_np = numpy.array(ids).astype('int64')            # аналогично для id
    index.add_with_ids(vectors_np, ids_np)            # добавляем вектора с id вместе
    faiss.write_index(index, path)               # сохраняем обратно в файл


def do_everything(session):
    chunks = read_chunks_from_file()
    vectors = get_vectors_from_chunks(chunks)
    ids = write_chunks_to_db(session, chunks)
    path = 'faiss.index'
    dimension = vectors[0].shape[0]  # определяем размерность по атрибуту формы вектора. Одинаковая для одной модели. Сменится модель - перезадать
    if not os.path.exists(path):
        create_faiss_index(dimension, path)
    add_vectors_to_faiss(vectors, ids, path)


def show_me_chunks(session, request):
    model = SentenceTransformer('models/all-MiniLM-L6-v2')
    embedding = model.encode(request, convert_to_numpy=True).astype('float32')
    embedding = embedding / numpy.linalg.norm(embedding)  # 🔧 нормализация

    index = faiss.read_index('faiss.index')

    k = 1
    D, I = index.search(embedding.reshape(1, -1), k)
    vector_ids = I[0].tolist()

    chunks = []
    for vector_id in vector_ids:
        statement = select(AIChunk).where(AIChunk.id == vector_id)
        result = session.execute(statement)
        chunk = result.scalar_one_or_none()
        if chunk is not None:
            chunks.append(chunk.chunk_text)
    return chunks


db_url = "sqlite:///../database/business_trips.db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
#do_everything(session=SessionLocal())

request = 'Кому предоставлять отчет об итогах командировки?'
print(show_me_chunks(session=SessionLocal(), request=request))

request = 'Кто подписывает приказ о командировке?'
print(show_me_chunks(session=SessionLocal(), request=request))