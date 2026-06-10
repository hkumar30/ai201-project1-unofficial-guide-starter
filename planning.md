# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Unofficial ASU Computer Science course planning and workload guide.

This project builds an unofficial ASU Computer Science course planning and workload guide for undergraduate students. It helps students understand degree requirements, major maps, course sequencing, prerequisites, General Studies requirements, academic support resources, and student-reported workload for courses such as CSE 310, CSE 330, CSE 340, CSE 355, and CSE 365. This knowledge is hard to find in one place because official requirements are spread across ASU degree pages, major maps, catalog pages, syllabi, and advising resources, while practical workload advice is scattered across Reddit threads and student-maintained course guides.

This domain is useful because ASU CS students often need both official information and student experience to make course-planning decisions. Official pages tell students what is required, but unofficial sources help answer practical questions about workload, difficulty, preparation, and whether certain course combinations may be too much in the same semester.

Official ASU sources are authoritative for degree requirements, prerequisites, catalog rules, major maps, advising information, and academic support resources. Reddit and student-maintained sources are only for student workload impressions, difficulty perception, preparation advice, common planning concerns, and unofficial course survival advice. If official sources and Reddit disagree, official ASU sources win.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | ASU Computer Science BS program page | Official ASU source; authoritative for program overview, degree framing, and major map context. Helps answer what the ASU CS BS program covers. | https://scai.engineering.asu.edu/computer-science-bs/ |
| 2 | ASU Computer Science BS program requirements, 2025-2026 | Official ASU catalog/degree source; authoritative for 2025-2026 degree requirements and credit structure. | https://degrees.apps.asu.edu/checksheet/2025/CES/ESCSEBS/null |
| 3 | ASU Computer Science BS major map, 2024-2025 | Official ASU catalog/degree source; authoritative for 2024-2025 semester-by-semester course sequencing. | https://degrees.apps.asu.edu/major-map/ASU00/ESCSEBS/null/ALL/2024 |
| 4 | SCAI CS BS degree requirements page | Official ASU source; authoritative for degree requirements, curriculum updates, and General Studies guidance. | https://scai.engineering.asu.edu/computer-science-bs/degree-requirements/ |
| 5 | ASU undergraduate General Studies requirement | Official ASU catalog source; authoritative for university-wide General Studies requirements. | https://catalog.asu.edu/ug_gsr |
| 6 | ASU Class Search: CSE courses | Official ASU catalog source; authoritative for term-specific CSE course offerings and catalog-style course information. | https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&honors=F&promod=F&searchType=all&subject=CSE&term=2257 |
| 7 | CSE 205 syllabus, Spring 2025 | Official ASU PDF; authoritative for Spring 2025 CSE 205 course-level details, topics, and expectations. | https://scai.engineering.asu.edu/wp-content/uploads/sites/31/2025/03/CSE-205-Syllabus-SP25.pdf |
| 8 | CSE 310 syllabus, Spring 2025 | Official ASU PDF; authoritative for Spring 2025 CSE 310 course-level details, topics, and expectations. | https://scai.engineering.asu.edu/wp-content/uploads/sites/31/2025/03/CSE-310-Syllabus-SP25.pdf |
| 9 | CSE 355 syllabus, Spring 2025 | Official ASU PDF; authoritative for Spring 2025 CSE 355 course-level details, topics, and expectations. | https://scai.engineering.asu.edu/wp-content/uploads/sites/31/2025/03/CSE-355-Syllabus-SP25.pdf |
| 10 | FSE PULSE Tutoring Centers | Official ASU source; authoritative for tutoring and academic support resources. | https://students.engineering.asu.edu/pulse/tutoring/ |
| 11 | SCAI Advising | Official ASU source; authoritative for advising resources and advising contacts. | https://scai.engineering.asu.edu/advising/ |
| 12 | SCAI Advising Appointments | Official ASU source; authoritative for how to schedule or understand SCAI advising appointments. | https://scai.engineering.asu.edu/scai-advising-appointments/ |
| 13 | CSE 340 Spring 2025 syllabus | Official ASU PDF; authoritative for Spring 2025 CSE 340 course-level details, topics, and expectations. | https://scai.engineering.asu.edu/wp-content/uploads/sites/31/2025/03/CSE-340-Syllabus-SP25.pdf |
| 14 | ASU CS Wiki: CSE 340 | Student-maintained unofficial source; useful for student-facing explanation of CSE 340 topics and expectations. | https://wiki.thesoda.io/courses/cse-340/ |
| 15 | Reddit: Are the CS trifecta courses really that hard? | Unofficial student-experience source; useful for student workload discussion about CSE 330, CSE 340, and CSE 355. | https://www.reddit.com/r/ASU/comments/tna185/are_the_computer_science_trifecta_courses_really/ |
| 16 | Reddit: CSE 340, 330, 355 | Unofficial student-experience source; useful for student discussion about differences between the "trifecta" courses. | https://www.reddit.com/r/ASU/comments/k8y7si/cse_340_330_355/ |
| 17 | Reddit: How to prepare for CSE 355 and CSE 340? | Unofficial student-experience source; useful for student preparation advice for CSE 355 and CSE 340. | https://www.reddit.com/r/ASU/comments/w89geu/how_to_prepare_for_cse_355_and_cse_340_what/ |
| 18 | Reddit: How do I prepare for CSE 355? | Unofficial student-experience source; useful for student advice about preparing for CSE 355. | https://www.reddit.com/r/ASU/comments/13yvlki/how_do_i_prepare_for_cse_355/ |
| 19 | Reddit: Preparation for CSE 310 | Unofficial student-experience source; useful for student preparation advice for CSE 310. | https://www.reddit.com/r/ASU/comments/18gk8ok/preparation_for_cse310/ |
| 20 | Reddit: Upper Division Technical Electives | Unofficial student-experience source; useful for student discussion of upper-division technical electives. | https://www.reddit.com/r/ASU/comments/dewiz2/upper_division_technical_electives/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

Use a structure-first chunking strategy with token caps instead of only fixed-length splitting. For long official pages, degree pages, major maps, and syllabus PDFs, target about 800 tokens per chunk with a hard maximum of about 1,000 tokens. For Reddit/student-experience sources, keep each original post or top-level comment as its own chunk when possible; only split a comment if it is unusually long, using a smaller target of about 350-500 tokens.

**Overlap:**

Use about 120 tokens of overlap for long official pages, syllabi, and wiki sections so that prerequisites, grading details, or course-topic explanations do not get separated from their surrounding context. Use little or no overlap for Reddit chunks when a chunk is already a complete post or comment, because duplicating short opinion text can overweight one student's view in retrieval.

**Reasoning:**

The document set is mixed: some sources are structured official pages or PDFs with many sections, while others are shorter student comments or course-guide pages. Official pages should be split by headings or requirement sections first, then capped by token count. Major maps and checksheets should be split by semester or requirement group. PDFs should be split by syllabus section if the headings extract cleanly; otherwise, page-level chunks are an acceptable fallback. Reddit threads should preserve comment boundaries because a single comment usually contains one student's complete workload impression or preparation tip.

Chunks that are too small would make retrieval miss context, such as a course prerequisite appearing in one chunk and the course name or catalog year appearing in another. Chunks that are too large would mix unrelated requirements, policies, course advice, and opinions, causing retrieval to return broad but unfocused context. The goal is for each chunk to answer one narrow question on its own while still preserving enough surrounding context for source-grounded generation.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

Use `all-MiniLM-L6-v2` through `sentence-transformers`. It is a good baseline for this project because it runs locally, is already represented in the project dependencies, is fast enough for a small student project corpus, and works well for semantic similarity over short-to-medium English text.

**Top-k:**

Retrieve the top 6 chunks per query from ChromaDB. Six chunks should usually provide enough context to combine official ASU requirements with one or two relevant unofficial student-experience chunks without overwhelming the generation step. For questions about requirements, prerequisites, advising, General Studies, or tutoring, the response should prefer official ASU chunks even if Reddit chunks also appear in the result set.

**Production tradeoff reflection:**

If this were deployed for real users and cost were not a constraint, I would compare models with longer context windows, stronger retrieval accuracy on academic/catalog language, and better handling of mixed formal and informal text. A larger hosted embedding model might improve matching between student phrasing and official catalog language, but it would add cost, latency, and API dependency. A local model keeps the project simple and reproducible, but it may be less accurate for nuanced course-planning questions. I would also test whether reranking retrieved chunks improves cases where Reddit opinions are semantically similar to a query but official ASU sources should be treated as more authoritative.

Semantic search helps because a student might ask "Is the trifecta too much?" even if a source says "CSE 330, CSE 340, and CSE 355 workload." Embeddings can place those related meanings near each other even when the exact words differ. Retrieving too few chunks could miss either the official requirement context or the student workload context; retrieving too many chunks could introduce noise and make the generated answer less focused.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which sources should be treated as authoritative for ASU CS degree requirements? | The correct answer should name the ASU Computer Science BS program requirements/checksheet, ASU major map, SCAI degree requirements page, ASU General Studies page, and ASU Class Search as official sources. It should also state that Reddit and the student wiki are not authoritative for degree requirements. |
| 2 | Which sources should answer questions about where to get tutoring for CSE courses? | The correct answer should point to the FSE PULSE Tutoring Centers source as the official tutoring and academic support source, not Reddit. |
| 3 | Which sources should answer questions about scheduling or using SCAI advising? | The correct answer should point to the SCAI Advising and SCAI Advising Appointments pages as the official advising sources. |
| 4 | What source types should be used to answer whether CSE 330, CSE 340, and CSE 355 are hard to take together? | The correct answer should use Reddit/student-experience threads only for unofficial workload impressions and should use official ASU sources for requirements, prerequisites, and schedule rules. It should not present Reddit opinions as official guidance. |
| 5 | What sources should be used for CSE 340 course content versus student preparation advice? | The correct answer should use the official CSE 340 Spring 2025 syllabus for course content and expectations, and the ASU CS Wiki or Reddit only for unofficial student-facing preparation context. |
| 6 | What sources should be used for CSE 310 course content and preparation advice? | The correct answer should use the official CSE 310 Spring 2025 syllabus for course content and the Reddit CSE 310 preparation thread only as unofficial student preparation advice. |
| 7 | What should the system say if official ASU sources and Reddit disagree about a requirement or prerequisite? | The correct answer should say that official ASU sources win, and the student should verify final schedule decisions with ASU advising. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

Reddit threads are noisy, subjective, and may be outdated. A future retrieval system might surface a confident student opinion that conflicts with official ASU requirements, so source type and authority metadata must be preserved and shown in responses.

2.

Different catalog years and terms can produce different requirements, course availability, or sequencing advice. If chunks do not preserve catalog year and term metadata, the system could mix a 2024-2025 major map with 2025-2026 requirements or a term-specific Class Search result.

3. PDF syllabi may not extract cleanly. If PDF headings, tables, or schedules are flattened badly, chunks could separate course topics from grading policies or prerequisites.

4. Chunk boundaries can damage retrieval quality. If chunks are too small, the system may retrieve a fragment without enough context; if they are too large, the system may retrieve a broad chunk that contains the right term but too much unrelated information.

5. Some pages may be dynamic or hard to scrape later. ASU catalog and class-search pages may need special handling during ingestion so the pipeline captures useful text and metadata instead of navigation or empty page content.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
Source URLs + local PDFs + data/sources.json
        |
        v
Document Ingestion
  Planned tools: Python, requests/BeautifulSoup for web pages, pdfplumber for PDFs,
  and source metadata from data/sources.json
        |
        v
Chunking
  Planned tool: custom Python chunker using source-type rules
  official pages by heading, major maps by semester/requirement group,
  PDFs by syllabus section/page, Reddit by post/comment
        |
        v
Embedding + Vector Store
  Planned tools: sentence-transformers all-MiniLM-L6-v2 + ChromaDB
        |
        v
Retrieval
  Planned tool: ChromaDB semantic similarity search, top-k = 6,
  with source authority metadata preserved
        |
        v
Generation
  Planned tool: Groq chat model with a grounding prompt,
  source citations, and official-source priority rules
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 - Ingestion and chunking:**

I plan to use an AI tool to help implement document ingestion and chunking. I will give it the Documents section, Chunking Strategy section, and Architecture diagram from this `planning.md`, plus the rule that Milestone 3 should not create embeddings, ChromaDB retrieval, Groq generation, or an interface unless those are explicitly assigned. I expect it to produce functions for loading source metadata, extracting text from HTML/PDF/local files, cleaning obvious boilerplate, and chunking text according to source type. I will verify the output by inspecting extracted text samples, checking chunk sizes, confirming source metadata is attached to every chunk, and making sure the chunker preserves official versus unofficial source labels.

**Milestone 4 - Embedding and retrieval:**

I plan to use an AI tool to help implement embeddings and vector search. I will give it the Retrieval Approach section, Architecture diagram, and the finalized chunk format from Milestone 3. I expect it to produce code that embeds chunks with `all-MiniLM-L6-v2`, stores them in ChromaDB with metadata, and retrieves the top 6 relevant chunks for a query. I will verify the output by running the evaluation questions and checking whether retrieved chunks come from the expected official or unofficial source categories.

**Milestone 5 - Generation and interface:**

I plan to use an AI tool to help implement grounded generation and a simple query interface. I will give it the source authority rules from the Domain section, the Retrieval Approach section, and the Evaluation Plan questions. I expect it to produce a prompt template and response function that uses retrieved context, cites sources, distinguishes official ASU information from student experience, and refuses to treat Reddit as authoritative for requirements. I will verify the output by checking that each evaluation response includes relevant citations and does not answer beyond the retrieved sources.
