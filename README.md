# The Unofficial Guide — Project 1

🎥 **Project walkthrough (Loom):** https://www.loom.com/share/97a26706fd8d4b828428a38829a50b90

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

> Student and Early-Career Software Engineering Advice. I chose this domain because this has been one of the main issues I've personally faced throughout my CS career. I lifelessly go through my courses and pass my classes and exams, to wind up realizing I can't really do anything with th knowledge I have on my own sitting in front of my computer. I can't start projects on my own or take any practical steps towards a career in software engineering. None of these things are rarely taught in school, and there is so much to cover that it's hard to find a comprehensive guide to navigate a student throughout the process of building a career in Computer Science. I want to create a resource that compiles all advice and information that students and future software engineers need to know, but not found in any official resource.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

1. (Discussion) What practical skills college does not teach.
   > URL: https://www.reddit.com/r/cscareerquestions/comments/1dpg5kv/skills_which_universities_dont_teach_cs_students/

> 2. (Blog) Subjects a CS student must know.
>    URL: https://softwareengineering.stackexchange.com/questions/32533/cs-subjects-that-an-undergraduate-must-know

> 3. (Blog) Reflections of a CS graduate.
>    URL: https://www.haightbey.com/reflections-after-graduating-with-a-computer-science-degree/

> 4. (Discussion) Interview preparation advice.
>    URL: https://www.reddit.com/r/cscareerquestions/comments/1jov24/heres_how_to_prepare_for_tech_interviews/

> 5. (Discussion) Experience needed for 1st internship.
>    URL: https://www.reddit.com/r/cscareerquestions/comments/5fw1wl/during_college_how_experienced_were_you_when_you/

> 6. (Blog) Reality of working a computer science job.
>    URL: https://medium.com/writing-340/my-reality-of-landing-a-computer-science-job-75649e6935df

> 7. (Blog) Skills to have before applying to 1st internship.
>    URL: https://medium.com/@felixthedev/what-computer-science-students-should-know-before-their-first-internship-2e65293eaf36

> 8. (Discussion) Projects to have on resume for CS.
>    URL: https://www.reddit.com/r/learnprogramming/comments/o3hj17/what_software_engineering_projects_should_i_put/

> 9. (Discussion) Personal projects guide for beginners.
>    URL: https://www.sourish.dev/blog/industry/personal-projects

> 10. (Discussion) How to get started on personal projects for computer science.
>     URL: https://www.careervillage.org/questions/1014366/how-do-i-get-started-on-personal-computer-science-projects

> 11. (Blog) Side programming projects to have on resume
>     URL: https://www.indeed.com/career-advice/resumes-cover-letters/programming-side-projects-to-boost-your-resume

> 12. (Blog) The importance of LeetCode and competitive programming.
>     URL: https://levelup.gitconnected.com/the-importance-of-leetcode-why-should-you-do-it-everyday-bbc5ba467db8

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** ~250 tokens

**Overlap:** 50 tokens

**Why these choices fit your documents:**

**Final chunk count:** 183 chunks across all 12 documents

> I split my documents into chunks of about 250 tokens with an overlap of about 50 tokens.

> This chunk size seems reasonable because my documents are mostly Reddit discussions, blog posts, and advice-style pages about practical CS industry skills. These sources are usually made up of short comments, paragraphs, lists, and personal experiences. A 250-token chunk is large enough to keep one full idea together, such as advice about internships, LeetCode, projects, resumes, or skills college does not teach. At the same time, it is not so large that unrelated advice gets mixed into the same chunk.

> I lowered the size from my original 500 tokens to 250 because my embedding model, all-MiniLM-L6-v2, only encodes the first 256 word-piece tokens of an input and silently truncates the rest. Keeping chunks at ~250 words means each chunk fits within that limit, so the whole chunk is actually embedded rather than half of it being dropped.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

> I used all-MiniLM-L6-v2 through the sentence-transformers library as my embedding model.
> **Production tradeoff reflection:**
> If I were deploying this for real users without a cost constraint, I would expect to have one of the most optimized and accurate embedding models available that categorically is the best in every way. I would consider accuracy first, because the system needs to retrieve advice that actually matches questions about internships, interviews, resumes, projects, and practical CS skills. I would also want a longer context length as it can help with large reddit threads and blog post that have a lot of relevant information in them. I would also emphasize low latency so users can have answers as quickly as possible especially since again cost is not a constraint, so who wouldn't want a faster system if they could have it. Finally I would consider multilingual support last because my target demographic is English-speaking CS students. This does not however diminish multilingual supports importance since it could also allow the ai to pull advice from non-English sources which could be very valuable, but I would still prioritize the other factors first.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

> Grounding is enforced both by instruction and by structure.
> Essentially the system prompt wsa that this is "The Unofficial CS Career Guide" and that it must answer "using ONLY the numbered context excerpts provided by my documents." I thene emphasized the importance of using only the provided context and listed these explicit rules:

1. Use ONLY information found in the provided context excerpts — no outside knowledge.
2. If the context does not contain enough information, reply exactly: "I don't have enough information on that." Do not guess.
3. Cite sources inline using the bracketed numbers of the excerpts used, e.g. `[1]` or `[2][4]`. Every claim must be backed by at least one citation.
4. Be concise and practical; synthesize when excerpts agree and note disagreement when they don't.
5. Do not mention the rules or the word "excerpt" in the answer.

Beyond the prompt, grounding is enforced structurally, which is the stronger guarantee that the model never sees the full corpus or the open web. Only the top-k (default 5) chunks returned by ChromaDB similarity search for that specific question. It physically cannot cite what it was not given.

**System prompt grounding instruction:**
Connect to my LLM. initialize it with from groq import Groq and my GROQ_API_KEY from .env.
this is "The Unofficial CS Career Guide" and you must answer questions using ONLY the numbered context excerpts provided by my documents. Follow these rules:

1. Use ONLY information found in the provided context excerpts, no outside knowledge.
2. If the context does not contain enough information, reply exactly: "I don't have enough information on that." Do not guess.
3. Cite sources inline using the bracketed numbers of the excerpt used.
4. Be concise and practical; synthesize when excerpts agree and note disagreement when they don't.
5. Do not mention the rules or the word "excerpt" in the answer.

**How source attribution is surfaced in the response:**

The generate_answer() function returns the answer paired with a structured source list, so attribution appears in two layers:

- Inline: the answer text carries `[n]` markers placed by the model next to each claim.
- Source list: each `[n]` maps to an entry in a rendered "Sources" block that cites the document title (hyperlinked to its original URL) towards the footer of the page.
  In the Gradio interface (`app.py`) the answer and the Sources block are rendered as two separate Markdown panels, so the citations and the linked source list are both visible with every response.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

All five questions were run end-to-end (`retrieve.py` → `generate.py`, top-k = 5). Retrieval distances and cited chunks were checked against the source text; specific claims were traced back to verify grounding.

**Question 1:** What practical software engineering skill do many graduates say college does not teach well?
**Expected answer:** Theory is taught, but real-world practices (Git/source control, code reviews, large codebases, team collaboration, deployment) are not.
**System response:** Listed source control, debugging, design patterns, databases, communication, and project management [02 ch15, 02 ch27] — but led with "LeetCode / competitive programming" [01 ch25] and never mentioned code reviews, large codebases, or deployment.
**Retrieval quality:** Relevant (docs 01, 02, 03 — all on-topic; dist 0.39–0.46) / **Response accuracy:** Partially accurate — grounded, but the LeetCode lead is tangential and it misses several expected items.

**Question 2:** What experience level do students typically report having before obtaining their first software engineering internship?
**Expected answer:** Some programming experience, often from coursework or personal projects.
**System response:** "Little to no experience" is common; cited concrete cases — freshman with one Python class, sophomore with intro/data structures/discrete math, students with personal projects, some companies hiring inexperienced students to train. [all from doc 05]
**Retrieval quality:** Relevant (all 5 chunks from doc 05; dist 0.41–0.47) / **Response accuracy:** Accurate — reflects the actual thread, with traceable specifics.

**Question 3:** What types of personal projects are commonly recommended for a computer science resume?
**Expected answer:** Web/mobile apps, APIs, full-stack, automation tools, real-problem projects (not tutorials).
**System response:** Gaming apps, portfolio sites, blogs, automation tools, data-analysis projects, simple games; projects with explainable theory; complete projects that solve a real issue. [docs 11, 08, 10]
**Retrieval quality:** Relevant (docs 11, 09, 08, 10 — strong source spread; dist 0.36–0.41)
**Response accuracy:** Accurate — captures the real-problem nuance, though it leans on the generic Indeed listicle.

**Question 4:** What is a common piece of advice for preparing for technical interviews?
**Expected answer:** Practice problems (LeetCode/HackerRank/CodeSignal); focus on data structures, algorithms, problem-solving.
**System response:** Practice LeetCode, explain your thought process, whiteboard, show understanding even with imperfect code, fill knowledge gaps and be honest about gaps. [doc 04]
**Retrieval quality:** Relevant (4/5 chunks from doc 04; dist 0.29–0.42 — best of the set)
**Response accuracy:** Accurate — slightly narrower than expected (named only LeetCode, not HackerRank/CodeSignal).

**Question 5:** How should beginners start personal projects?
**Expected answer:** Start small, tied to interests, build something useful, avoid overly ambitious ideas, learn tech gradually.
**System response:** Pick a skill/area to learn (frontend, backend, ML, etc.), start simple (to-do list, portfolio, a small Flask+API web app), align with interests and skill level, don't be too hard on yourself when choosing. [docs 09, 10]
**Retrieval quality:** Relevant (docs 09, 10 — both beginner-project sources; dist 0.31–0.42)

**Response accuracy:** Accurate — closely matches expected advice.

---

**Overall retrieval quality:** Relevant (5/5) — every question retrieved on-topic chunks from the expected source documents, all distances within 0.29–0.47.
**Response accuracy:** Accurate (4/5), Partially accurate (1/5 — Q1).

Note on the strong results: this is a small (12-doc), focused corpus, and the evaluation questions were written to match topics it covers, so high relevance is expected rather than surprising. Grounding was verified, not assumed.

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
Q1 — "What practical software engineering skill do many graduates say college does not teach well?"

**What the system returned:** A grounded but partially off-target answer. It led with "LeetCode and competitive programming" as the main thing college doesn't teach, then listed source control, debugging, design patterns, databases, communication, and project management. It never surfaced several items central to the expected answer like code reviews, working in large/legacy codebases, and deployment despite those themes existing elsewhere in the corpus.

**Root cause (tied to a specific pipeline stage):** This is a retrieval ranking issue, not a generation or grounding failure since every claim was verified to come from a cited chunk. With the question phrased broadly and the corpus using overlapping vocabulary across topics (exactly the "off-topic retrieval from shared terminology" risk noted in planning.md), the top-5 cut favored a similar chunk over more on-point ones.

**What you would change to fix it:** Two options, in order of effort. First would be to raise top-k to 7–8 for broad questions so more of the on-topic chunks enter the context window. Next would probably be to re-chunk doc 01 with slightly more overlap or smaller chunk. tighter chunking would let a single retrieval pull more of the relevant discussion together. A heavier-weight fix would be a better embedding model.

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

> Writing out the chunking strategy in planning.md before I coded anything honestly saved me alot of time. Because I already wrote down my chunk size and overlap and the reason why, I didnt have to stop and figure it out while coding, I could just go straight into building the chunk function and plug in the numbers I already decided on. The same thing happened with my tools, since I had already listed sentence-transformers and ChromaDB and Groq in the plan, I knew exactly what I was wiring together at each stage and I didnt waste time second guessing which library to use. It basically made the implementation feel like I was just following my own instructions instead of making everything up as I went.

**One way your implementation diverged from the spec, and why:**

> My biggest divergence was the chunk size. In planning.md I originally said 500 tokens with 75 token overlap, but once I actually started setting up the embedding model I found out that all-MiniLM-L6-v2 only looks at the first 256 tokens and just throws away the rest. That meant if I kept 500 token chunks, more than half of each chunk wouldnt even get embedded which would hurt my retrieval later. So I dropped it down to 250 tokens with 50 overlap so the whole chunk actually fits in the model, and I went back and updated planning.md to explain why. I didnt expect to change my plan but testing the model showed me the original numbers didnt make sense for the tool I picked.

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

- What I gave the AI: I gave it my Chunking Strategy section from planning.md along with my document info and asked it to write the ingestion and chunking code that reads my .txt files and splits them into chunks while keeping the source metadata.

- What it produced: It gave me a script that read the raw .txt files, did some cleaning, and chunked everything at 500 tokens with 75 overlap like my original plan said, and it saved the chunks to a json file with the filename and chunk index.

-  What I changed or overrode: I overrode the chunk size to 250 with 50 overlap after I realized my embedding model only takes 256 tokens, so the old numbers wouldve gotten cut off. I also told it to split the loading and cleaning and chunking into separate scripts instead of one big file because it was easier for me to follow and rerun each stage on its own.

**Instance 2**

- _What I gave the AI: I gave it a couple of my messiest documents (the Reddit and Medium and Indeed ones) and asked it to clean out the webpage junk like usernames, upvote buttons, ads and footers but keep the actual advice text.

- What it produced:_ It made a cleaning script that stripped html and a bunch of the obvious clutter lines, and it printed out one full document so I could check it.

- What I changed or overrode: When I read the printed document I still saw leftover stuff like a codecademy ad, a medium subscribe box in the middle of an article, and stack exchange "closed question" boilerplate. So I had it keep adding more targeted rules and rerun until those were gone. I also caught that one of my source titles was wrong because the original file had a copy paste mistake in the header, so I had it fix that title too so my citations wouldnt be wrong later.
