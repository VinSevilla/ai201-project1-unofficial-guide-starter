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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

> 250 Tokens
> **Overlap:**
> 50 Tokens
> **Final chunk count:**
> 183 chunks across all 12 documents.
> **Reasoning:**
> I will split my documents into chunks of about 250 tokens with an overlap of about 50 tokens.

> This chunk size seems reasonable because my documents are mostly Reddit discussions, blog posts, and advice-style pages about practical CS industry skills. These sources are usually made up of short comments, paragraphs, lists, and personal experiences. A 250-token chunk is large enough to keep one full idea together, such as advice about internships, LeetCode, projects, resumes, or skills college does not teach. At the same time, it is not so large that unrelated advice gets mixed into the same chunk.

> I lowered the size from my original 500 tokens to 250 because my embedding model, all-MiniLM-L6-v2, only encodes the first 256 word-piece tokens of an input and silently truncates the rest. Keeping chunks at ~250 words means each chunk fits within that limit, so the whole chunk is actually embedded rather than half of it being dropped.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

> I will use all-MiniLM-L6-v2 through the sentence-transformers library as my embedding model.
> **Top-k:**
> 5 chunks per query.
> **Production tradeoff reflection:**
> If I were deploying this for real users without a cost constraint, I would expect to have one of the most optimized and accurate embedding models available that categorically is the best in every way. I would consider accuracy first, because the system needs to retrieve advice that actually matches questions about internships, interviews, resumes, projects, and practical CS skills. I would also want a longer context length as it can help with large reddit threads and blog post that have a lot of relevant information in them. I would also emphasize low latency so users can have answers as quickly as possible especially since again cost is not a constraint, so who wouldn't want a faster system if they could have it. Finally I would consider multilingual support last because my target demographic is English-speaking CS students. This does not however diminish multilingual supports importance since it could also allow the ai to pull advice from non-English sources which could be very valuable, but I would still prioritize the other factors first.

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

> Question 1: What practical software engineering skill do many graduates say college does not teach well?
> Expected answer: Many sources mention that universities focus on theory and programming fundamentals but do not adequately teach real-world software development practices such as Git, code reviews, working in large codebases, team collaboration, and software deployment.

> Question 2: What experience level do students typically report having before obtaining their first software engineering internship?
> Expected answer: Students typically report having some programming experience, often gained through coursework or personal projects, before obtaining their first software engineering internship.

> Question 3: What types of personal projects are commonly recommended for a computer science resume?
> Expected answer: Projects that demonstrate practical software development skills are most commonly recommended. Examples include web applications, mobile apps, APIs, full-stack projects, automation tools, and projects that solve real problems rather than simple tutorial projects.

> Question 4: What is a common piece of advice for preparing for technical interviews?
> Expected answer: A common piece of advice is to practice coding problems regularly on platforms like LetCode, HackerRank, or CodeSignal, and to focus on data structures, algorithms, and problem-solving skills.

> Question 5: How should beginners start personal projects?
> Expected answer: Students are often advised to start with a small project related to their own interests, focus on building something useful, avoid overly ambitious ideas, and learn new technologies gradually while developing the project.

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Especially with Reddit discussions, there may be a lot of noise and off-topic information in the documents. This could lead to chunks that contain irrelevant advice or personal anecdotes that do not answer users' questions about internships, projects, resumes, or interview preparation.

2. A second risk is off-topic retrieval caused by overlapping terminology. Many documents discuss internships, projects, interviews, resumes, and technical skills using similar language. A question about internship preparation could accidentally retrieve chunks about personal projects or LeetCode because they share related keywords.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

>

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

> For document ingestion, I plan to use ChatGPT or Claude to help write the code that loads my collected Reddit discussions, blog posts, and career advice articles into the project. I will give the AI my document list, my domain description, and the requirement that each document should keep its title, URL, source type, and text content. I expect it to produce a function that reads the documents from files or scraped text and stores them in a consistent format. I will verify this by printing the number of loaded documents, checking that all 12 sources appear, and confirming that each document still has its original URL for citation.

> For chunking, I plan to use Claude or ChatGPT to implement a chunk_text() function. I will give it my chunking strategy section, including my chosen chunk size of 500 tokens and overlap of 75 tokens. I expect it to produce code that splits each document into overlapping chunks while preserving metadata such as source title and URL. I will verify this by checking several chunks manually to make sure they are not empty, not too large, and still contain enough context to understand the advice.

> For embedding and vector storage, I plan to use AI assistance to connect sentence-transformers with ChromaDB. I will give it my architecture diagram, the recommended stack, and my chosen embedding model, all-MiniLM-L6-v2. I expect it to produce code that embeds each chunk and saves the embeddings into a ChromaDB collection. I will verify this by checking that the collection contains the same number of items as my chunk list and by running a simple test query to confirm that similar chunks are returned.

> For retrieval, I plan to ask ChatGPT or Claude to implement a retrieval function using ChromaDB similarity search. I will give it my retrieval specification that says the system should return the top 5 chunks for each user query. I expect it to produce a function that accepts a natural-language question and returns the five most relevant chunks with their titles and URLs. I will verify this by running my five test questions and checking whether the retrieved chunks come from the expected supporting documents.

> For generation, I plan to use AI assistance to write the prompt that sends the user question and retrieved chunks to Groq using llama-3.3-70b-versatile. I will give the AI my evaluation questions, expected answers, and the requirement that generated answers must be grounded in retrieved sources. I expect it to produce a generation function that answers the question using only the retrieved context and includes source citations. I will verify this by comparing the output against my expected answers and checking that every major claim is supported by a retrieved chunk.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
