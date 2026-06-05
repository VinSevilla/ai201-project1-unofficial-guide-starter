# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

> Unofficial CS Career Guide: Student and Early-Career Software Engineering Advice. I chose this domain because this has been one of the main issues I've personally faced throughout my CS career. I lifelessly go through my courses and pass my classes and exams, to wind up realizing I can't really do anything with th knowledge I have on my own sitting in front of my computer. I can't start projects on my own or take any practical steps towards a career in software engineering. None of these things are rarely taught in school, and there is so much to cover that it's hard to find a comprehensive guide to navigate a student throughout the process of building a career in Computer Science. I want to create a resource that compiles all advice and information that students and future software engineers need to know, but not found in any official resource.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

> 1. (Discussion) What practical skills college does not teach.
>    URL: https://www.reddit.com/r/cscareerquestions/comments/1dpg5kv/skills_which_universities_dont_teach_cs_students/

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
>    URL: https://medium.com/writing-340/my-reality-of-landing-a-computer-science-job-75649e6935df

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

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

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
