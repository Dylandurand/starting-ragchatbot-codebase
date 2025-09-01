#!/usr/bin/env python3
"""Test script to debug the lesson link functionality"""

import sys
import os
sys.path.append('backend')

from document_processor import DocumentProcessor
from vector_store import VectorStore
from search_tools import CourseSearchTool
from config import Config

# Initialize components
config = Config()
doc_processor = DocumentProcessor(config.chunk_size, config.chunk_overlap)
vector_store = VectorStore(config.chroma_db_path, config.embedding_model, config.max_search_results)

# Process a course document
print("Processing course document...")
course, chunks = doc_processor.process_course_document("docs/course1_script.txt")

print(f"Course: {course.title}")
print(f"Lessons: {len(course.lessons)}")
for lesson in course.lessons:
    print(f"  Lesson {lesson.lesson_number}: {lesson.title}")
    print(f"    Link: {lesson.lesson_link}")

# Add to vector store
print("\nAdding to vector store...")
vector_store.add_course_metadata(course)
vector_store.add_course_content(chunks)

# Test search and formatting
print("\nTesting search...")
search_tool = CourseSearchTool(vector_store)
result = search_tool.execute("introduction")
print("Search result:")
print(result)

print("\nLast sources:")
for source in search_tool.last_sources:
    print(f"  '{source}'")
    if '|' in source:
        parts = source.split('|')
        print(f"    Display: '{parts[0]}'")
        print(f"    URL: '{parts[1]}'")