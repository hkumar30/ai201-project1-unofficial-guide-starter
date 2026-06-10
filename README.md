# The Unofficial Guide: ASU Computer Science Course Planning and Workload Guide 

This project is a small RAG system for ASU Computer Science undergraduate course planning. It combines official ASU sources with unofficial student-experience sources so students can ask grounded questions about degree requirements, sequencing, advising, tutoring, and course workload.

![alt text](/demo-ss.png)
<p style="text-align: center;">Figure 1. GUI of the Unofficial Guide</p>

Demo Link: https://www.youtube.com/watch?v=iPOysvXrRjM

## Domain

The domain is an unofficial ASU Computer Science course planning and workload guide. It is useful because ASU CS students often need both official rules and practical student experience before making schedule decisions. Official ASU pages explain requirements, prerequisites, major maps, General Studies rules, advising, and tutoring, but they do not usually answer questions like whether CSE 330, CSE 340, and CSE 355 feel manageable together.

This knowledge is hard to find in one place because the official information is spread across ASU degree pages, major maps, catalog pages, syllabi, advising pages, and tutoring pages. The unofficial information is scattered across Reddit threads and a student-maintained course wiki. The system treats official ASU sources as authoritative for requirements and uses Reddit/student-maintained sources only for workload impressions, preparation advice, and student perspective.

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | ASU Computer Science BS program page | Official ASU source | https://scai.engineering.asu.edu/computer-science-bs/ |
| 2 | ASU Computer Science BS program requirements, 2025-2026 | Official ASU catalog/degree source | https://degrees.apps.asu.edu/checksheet/2025/CES/ESCSEBS/null |
| 3 | ASU Computer Science BS major map, 2024-2025 | Official ASU catalog/degree source | https://degrees.apps.asu.edu/major-map/ASU00/ESCSEBS/null/ALL/2024 |
| 4 | SCAI CS BS degree requirements page | Official ASU source | https://scai.engineering.asu.edu/computer-science-bs/degree-requirements/ |
| 5 | ASU undergraduate General Studies requirement | Official ASU catalog source | https://catalog.asu.edu/ug_gsr |
| 6 | ASU Class Search: CSE courses | Official ASU catalog source | https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&honors=F&promod=F&searchType=all&subject=CSE&term=2257 |
| 7 | CSE 205 syllabus, Spring 2025 | Official ASU PDF | documents/CSE-205-Syllabus-SP25.pdf |
| 8 | CSE 310 syllabus, Spring 2025 | Official ASU PDF | documents/CSE-310-Syllabus-SP25.pdf |
| 9 | CSE 355 syllabus, Spring 2025 | Official ASU PDF | documents/CSE-355-Syllabus-SP25.pdf |
| 10 | FSE PULSE Tutoring Centers | Official ASU source | https://students.engineering.asu.edu/pulse/tutoring/ |
| 11 | SCAI Advising | Official ASU source | https://scai.engineering.asu.edu/advising/ |
| 12 | SCAI Advising Appointments | Official ASU source | https://scai.engineering.asu.edu/scai-advising-appointments/ |
| 13 | CSE 340 Spring 2025 syllabus | Official ASU PDF | documents/CSE-340-Syllabus-SP25.pdf |
| 14 | ASU CS Wiki: CSE 340 | Student-maintained unofficial source | https://wiki.thesoda.io/courses/cse-340/ |
| 15 | Reddit: Are the CS trifecta courses really that hard? | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/tna185/are_the_computer_science_trifecta_courses_really/ |
| 16 | Reddit: CSE 340, 330, 355 | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/k8y7si/cse_340_330_355/ |
| 17 | Reddit: How to prepare for CSE 355 and CSE 340? | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/w89geu/how_to_prepare_for_cse_355_and_cse_340_what/ |
| 18 | Reddit: How do I prepare for CSE 355? | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/13yvlki/how_do_i_prepare_for_cse_355/ |
| 19 | Reddit: Preparation for CSE 310 | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/18gk8ok/preparation_for_cse310/ |
| 20 | Reddit: Upper Division Technical Electives | Reddit/student-experience source | https://www.reddit.com/r/ASU/comments/dewiz2/upper_division_technical_electives/ |

The pipeline loaded 19 of the 20 sources. Source 6, ASU Class Search, produced only 2 cleaned tokens because the page is dynamic or blocked, so the pipeline recorded it as a load error instead of creating empty or misleading chunks.

## Chunking Strategy

**Chunk size:**

Official pages, degree pages, syllabi, and wiki pages: target 800 tokens, hard max 1,000 tokens. Reddit/student-experience sources: target 450 tokens, hard max 550 tokens.

**Overlap:**

Official/wiki/PDF chunks: 120 tokens. Reddit chunks: 0 tokens.

**Why these choices fit your documents:**

Official ASU pages and syllabi are long and structured, so larger chunks preserve requirements, course topics, and surrounding context. Reddit threads are shorter and opinion-based, so smaller chunks keep student advice focused without overweighting repeated comments.

**Final chunk count:**

51 chunks across 19 loaded documents. Chunk sizes ranged from 187 to 818 tokens, with an average of 614.5 tokens.

## Embedding Model

**Model used:**

`all-MiniLM-L6-v2` through `sentence-transformers`, stored in ChromaDB. Retrieval returns up to 5 chunks per query.

**Production tradeoff reflection:**

For a real deployment, I would test a larger embedding model against my evaluation questions to see whether it retrieves ASU catalog pages and Reddit advice more reliably. I would also weigh context length, latency, privacy, cost, and whether source-diverse reranking would reduce duplicate results from the same source.

## Grounded Generation

**System prompt grounding instruction:**

Groq `llama-3.3-70b-versatile` is instructed to answer only from retrieved context, avoid outside knowledge, and say `I don't have enough information in the provided sources to answer that.` when the context is insufficient.

The prompt also says official ASU sources are authoritative for requirements, prerequisites, catalog rules, advising, and support resources. Reddit and student-maintained sources are limited to workload impressions and preparation advice.

**How source attribution is surfaced in the response:**

Each retrieved chunk is labeled `[S1]`, `[S2]`, etc. The model cites those labels in the answer, and `query.py` also returns a separate source list with title, chunk index, distance score, and URL for the Gradio interface.

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which sources should be treated as authoritative for ASU CS degree requirements? | Should name the ASU CS program requirements/checksheet, major map, SCAI degree requirements page, ASU General Studies page, and ASU Class Search; should say Reddit/wiki are not authoritative. | Cited the ASU major map, ASU program requirements/checksheet, and General Studies page. It correctly said official ASU sources take precedence and recommended verifying schedule changes with advising, but it did not mention SCAI degree requirements or ASU Class Search. | Partially relevant | Partially accurate |
| 2 | Which sources should answer questions about where to get tutoring for CSE courses? | Should point to FSE PULSE Tutoring Centers as the official tutoring and academic support source, not Reddit. | Correctly cited FSE PULSE Tutoring Centers and described free drop-in tutoring, workshops, review sessions, online/on-campus support, and CSE course support. | Relevant | Accurate |
| 3 | Which sources should answer questions about scheduling or using SCAI advising? | Should point to SCAI Advising and SCAI Advising Appointments as the official advising sources. | Correctly cited SCAI Advising Appointments and SCAI Advising. It described the online appointment scheduling tool, ASURITE login, contact information, and preparing for a meeting. | Relevant | Accurate |
| 4 | What source types should be used to answer whether CSE 330, CSE 340, and CSE 355 are hard to take together? | Should use Reddit/student-experience sources only for unofficial workload impressions and official ASU sources for requirements, prerequisites, and schedule rules. | Retrieved Reddit/student-experience chunks and correctly framed them as student impressions about difficulty, workload, starting projects early, office hours, and study groups. It did not explicitly add that official ASU sources should still be used for requirements, prerequisites, and schedule rules. | Relevant | Partially accurate |
| 5 | What sources should be used for CSE 340 course content versus student preparation advice? | Should use the official CSE 340 Spring 2025 syllabus for course content and the ASU CS Wiki or Reddit only for unofficial preparation context. | Correctly separated the official CSE 340 syllabus for course content from Reddit/student wiki sources for preparation advice. It also stated that official ASU sources win if unofficial sources disagree. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

I also tested an out-of-domain question: `Which ASU dining hall has the best late-night food?` The system returned `I don't have enough information in the provided sources to answer that.` This is the desired behavior because dining halls are outside the collected ASU CS course-planning corpus.

## Failure Case Analysis

**Question that failed:** Which sources should be treated as authoritative for ASU CS degree requirements?

**What the system returned:** The system returned a partially correct answer citing the ASU major map, ASU Computer Science BS program requirements/checksheet, and ASU undergraduate General Studies requirement. It correctly treated official ASU sources as authoritative, but it omitted the SCAI CS BS degree requirements page and ASU Class Search, both of which were part of the expected answer.

**Root cause tied to the pipeline:** This failure comes from both ingestion and retrieval. ASU Class Search was collected as a source, but the ingestion pipeline could not extract useful text from it because the dynamic page cleaned down to only 2 tokens, so no Class Search chunk was available to retrieve. The SCAI degree requirements page did load, but the top-5 retrieval set was crowded by duplicate major-map and General Studies chunks. Because the reranker prioritizes source authority but does not enforce source diversity, multiple chunks from the same official sources displaced another relevant official source.

**What I would change to fix it:** I would add a manual or API-backed fallback for dynamic ASU Class Search pages so term-specific course offerings can be represented as local text or structured JSON. I would also add source-diverse reranking, such as limiting results to one or two chunks per source or using maximal marginal relevance, so the top-k set covers more distinct official sources. For degree-requirement questions, I would also add query routing that boosts the SCAI degree requirements page specifically.

## Spec Reflection

**One way the spec helped during implementation:** The `planning.md` spec made the source-authority rules clear before code was written. Because the spec said official ASU sources win for requirements and Reddit is only for student experience, I preserved `source_type` and `authority_level` metadata through ingestion, chunking, ChromaDB storage, retrieval, generation, and the UI. That planning also shaped the generation prompt, which explicitly distinguishes official ASU information from unofficial student-experience information.

The chunking and retrieval sections also gave the implementation concrete targets. The planned chunk sizes led to source-specific chunking rules instead of a generic fixed-character splitter, and the planned top-k retrieval became a measurable checkpoint during Milestone 4. When tutoring retrieval initially returned course syllabi instead of the official PULSE tutoring page, it showed that my retriever was not following the authority rules I wrote in `planning.md`.

**One way the implementation diverged from the spec, and why:** The original retrieval plan was mostly plain ChromaDB semantic top-k retrieval. During testing, pure semantic retrieval sometimes returned chunks that were topically related but not the best authority source; for example, syllabi that mentioned tutoring could outrank the official tutoring page. I diverged by adding query expansion, metadata-aware reranking, and an inspection threshold so official pages are preferred for official questions.

Another divergence is that the ASU Class Search source was listed in the source manifest but did not become a usable chunk. The page appears dynamic or blocked in the simple ingestion path, so the pipeline recorded the failure instead of fabricating content. I documented the missing source instead of claiming it was covered.

## AI Usage

**Instance 1**

- *What I gave the AI:* I gave the AI the Milestone 3 requirements, the Documents section from `planning.md`, the source list, and the chunking strategy with target token sizes and overlap.
- *What it produced:* It helped draft a Python ingestion and chunking pipeline that loads source metadata, fetches/extracts text, cleans documents, writes raw/clean JSONL files, and produces `data/chunks.jsonl`.
- *What I changed or overrode:* I kept the implementation tied to the milestone and did not add embeddings or ChromaDB during Milestone 3. I also directed the pipeline to keep source authority metadata in every chunk, use smaller no-overlap chunks for Reddit, save inspection reports, and record the ASU Class Search failure instead of producing empty chunks.

**Instance 2**

- *What I gave the AI:* I gave the AI the Retrieval Approach section, the architecture diagram, and the finalized chunk format from Milestone 3.
- *What it produced:* It helped create the ChromaDB embedding and retrieval script using `all-MiniLM-L6-v2`, persistent ChromaDB storage, source metadata, top-k retrieval, and a retrieval report.
- *What I changed or overrode:* I adjusted the implementation after inspecting real retrieval results. The first tutoring query buried FSE PULSE under course pages, so I changed the retriever to query extra candidates, use metadata-aware reranking, apply a distance threshold, and update `planning.md` from top-k 6 to top-k 5 to match the milestone guidance.

**Instance 3**

- *What I gave the AI:* I gave the AI the Milestone 5 grounding requirement, source-authority rules, the retrieval function, the Groq model requirement, and the Gradio interface skeleton.
- *What it produced:* It helped wire retrieval to Groq generation and build a Gradio UI with answer and source panes.
- *What I changed or overrode:* I tightened the system prompt so the model must answer only from retrieved context and must use the exact insufficient-information sentence when context is missing. I also made source attribution programmatic in `query.py` instead of relying only on the model, added a smoke-test script, and verified an out-of-domain dining hall question declined instead of hallucinating.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with:

```bash
GROQ_API_KEY=your_key_here
```

Build or refresh the document pipeline:

```bash
python scripts/build_document_pipeline.py
```

Build or refresh the vector store:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/build_vector_store.py
```

Run the Gradio app:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python app.py
```

Open `http://127.0.0.1:7860`.

Run the final evaluation script:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/test_generation.py
```
