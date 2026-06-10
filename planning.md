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

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What courses should an ASU CS student take in the first two years? | The answer should use the official ASU major map and degree requirements to describe a semester-by-semester lower-division sequence, while reminding students to verify catalog-year details with advising. |
| 2 | What are the prerequisites for CSE 310, CSE 340, CSE 355, or CSE 365? | The answer should rely on official ASU catalog, degree, class-search, or syllabus sources for prerequisites and should not treat Reddit as authoritative. |
| 3 | Should I take CSE 330, CSE 340, and CSE 355 in the same semester? | The answer should separate official requirement information from unofficial student workload impressions and recommend verifying schedule decisions with SCAI advising. |
| 4 | What does CSE 310 cover, and how should I prepare for it? | The answer should combine official CSE 310 syllabus information with clearly labeled unofficial student preparation advice. |
| 5 | What does CSE 355 cover, and why do students find it difficult? | The answer should use the official CSE 355 syllabus for course content and Reddit only for subjective difficulty or workload impressions. |
| 6 | What is CSE 340 like, and how should I prepare for it? | The answer should use the official CSE 340 syllabus for course structure and the ASU CS Wiki or Reddit only for unofficial preparation context. |
| 7 | Where can I get tutoring for CSE courses? | The answer should cite official ASU tutoring and academic support resources such as FSE PULSE. |
| 8 | How do I schedule or use SCAI advising? | The answer should cite official SCAI advising and advising appointment pages. |
| 9 | What General Studies requirements do ASU CS students need? | The answer should use official ASU General Studies and CS degree requirement pages, with attention to catalog-year differences. |
| 10 | Which technical electives do students discuss as manageable or difficult? | The answer may summarize Reddit discussion as unofficial student experience and should avoid presenting opinions as official guidance. |
| 11 | What information should I verify with official ASU advising before changing my schedule? | The answer should identify requirements, prerequisites, catalog year, course availability, transfer credit, and graduation impact as items to confirm with advising. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
