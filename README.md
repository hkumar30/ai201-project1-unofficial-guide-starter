# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
     
Student-reported workload, difficulty, and planning advice for Arizona State University Computer Science courses - valuable because official ASU sources cover requirements and prerequisites but don't reflect real course demands, common pitfalls, or whether certain combinations are too heavy to take together.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
