import json
import os
import re

# Precise IT & Business definitions for specialized/common vocabulary
CORE_DEFS = {
    "schedule": "To plan or arrange an event or task for a specific time; a structured timetable of planned activities.",
    "colleague": "A co-worker or professional associate within the same organization or team.",
    "issue": "A problem, software bug, or technical concern encountered during development or operations.",
    "feature": "A distinctive characteristic, software capability, or functional addition to a product.",
    "actually": "In fact or really; used to emphasize what is true or what happened as opposed to what was expected.",
    "focus": "To concentrate attention, effort, or resources on a particular task, project, or objective.",
    "process": "A series of systematic, structured steps or workflows taken in order to achieve a particular end.",
    "priority": "A task, goal, or requirement that is regarded as more urgent or important than others.",
    "specific": "Clearly defined, detailed, or exact; relating uniquely to a particular subject or item.",
    "environment": "The configuration of hardware, software, and network settings where an application runs (e.g., development, staging, production).",
    "develop": "To write, engineer, build, or advance software code, applications, or technical solutions.",
    "implement": "To put a decision, plan, technical specification, or code architecture into concrete effect.",
    "requirement": "A documented functional or non-functional specification that a software system must fulfill.",
    "scenario": "A postulated sequence of events or user flow used for system design, analysis, or testing.",
    "available": "Ready for immediate use, deployment, or access; not currently occupied or offline.",
    "suggest": "To put forward an idea, technical proposal, or approach for consideration by the team.",
    "concern": "A matter of interest, worry, or risk regarding system reliability, security, or project scope.",
    "basically": "In the most fundamental respects; used to summarize or simplify a complex technical concept.",
    "obviously": "In a way that is easily seen, recognized, or understood by everyone involved.",
    "architecture": "The structural design and organization of software components, databases, and system interfaces.",
    "infrastructure": "The underlying physical or virtual server hardware, cloud services, and networking required to operate software systems.",
    "performance": "The speed, responsiveness, throughput, and efficiency with which a software system executes tasks.",
    "repository": "A central storage location (such as Git) where source code, commits, and project files are managed and versioned.",
    "integrate": "To combine distinct software modules, APIs, or systems so that they work together seamlessly.",
    "estimate": "To calculate or predict the approximate time, cost, or effort required to complete a software task.",
    "previous": "Existing or occurring before in time or order (e.g., the prior software release or version).",
    "comfortable": "Feeling confident, relaxed, and proficient when using a specific technology or handling a task.",
    "definitely": "Without doubt; certainly and unquestionably accurate or agreed upon.",
    "interesting": "Arousing curiosity, technical engagement, or analytical interest.",
    "deprecate": "To discourage the use of a software feature or API because it has been superseded or is planned for future removal.",
    "deprecated": "Marked as obsolete and discouraged from use in new development, though still temporarily maintained for backward compatibility.",
    "refactor": "To restructure existing source code to improve readability and internal quality without changing its external behavior.",
    "refactoring": "The process of cleaning, optimizing, and restructuring internal source code without modifying runtime behavior.",
    "debug": "To identify, analyze, and remove bugs, logic errors, or defects from source code or system configurations.",
    "debugging": "The systematic process of locating, diagnosing, and resolving software defects and malfunctions.",
    "deploy": "To release, install, and configure software build artifacts onto a target environment such as staging or production.",
    "deployment": "The execution process of moving software updates from development pipelines to live server environments.",
    "backend": "The server-side logic, database interaction, API endpoints, and infrastructure behind a software application.",
    "frontend": "The user-facing visual interface, client-side scripts, and layout components of a web or mobile application.",
    "database": "An organized, structured collection of data stored electronically and accessed via querying engines.",
    "query": "A precise request for data retrieval or manipulation sent to a database or information system.",
    "latency": "The time delay experienced between initiating a data request over a network and receiving the initial response.",
    "throughput": "The rate at which data or tasks are successfully processed through a system or network connection.",
    "bandwidth": "The maximum volume of data that can be transmitted over a network connection in a given amount of time.",
    "endpoint": "A specific network URL or URI where an API service listens for and responds to client requests.",
    "payload": "The actual data body transmitted within an API request or network packet, excluding headers and metadata.",
    "parameter": "A variable or input value passed into a function, method, or API request to control its execution behaviour.",
    "variable": "A named symbolic storage location in memory used to hold dynamic data values during code execution.",
    "function": "A self-contained block of reusable code designed to perform a specific computational task when invoked.",
    "module": "An independent, interchangeable software file or package containing organized code definitions and utilities.",
    "dependency": "A third-party library, package, or service that a software project relies on to compile or execute properly.",
    "framework": "A comprehensive software platform or architectural foundation providing pre-built structure and tools for development.",
    "library": "A curated collection of reusable pre-written code routines and helper functions imported into an application.",
    "algorithm": "A finite, step-by-step sequence of logical computational instructions designed to solve a problem.",
    "sync": "To coordinate data or processes so they occur simultaneously or reflect exact identical states across systems.",
    "async": "Short for asynchronous; executing tasks independently without blocking the main program flow while waiting for completion.",
    "callback": "A function passed as an argument into another function to be executed once an asynchronous operation completes.",
    "promise": "An object representing the eventual completion or failure of an asynchronous operation and its resulting value.",
    "thread": "The smallest unit of execution managed independently by an operating system scheduler within a process.",
    "concurrency": "The capability of a system to handle multiple tasks or threads making progress during overlapping timeframes.",
    "parallelism": "The simultaneous physical execution of multiple computational tasks on separate CPU cores at the exact same instant.",
    "cache": "A high-speed temporary data storage layer used to serve future requests for the same data much faster.",
    "caching": "The practice of storing frequently accessed data in fast temporary memory to reduce latency and database load.",
    "session": "A semi-permanent interactive state maintained between a client device and a server over a period of time.",
    "token": "A cryptographic piece of data (such as a JWT) used to authenticate identity or authorize access rights.",
    "authentication": "The verification process of verifying that a user or system is accurately who they claim to be.",
    "authorization": "The access control process of determining whether an authenticated user has permission to perform a specific action.",
    "encryption": "The process of converting plain text data into unreadable ciphertext to prevent unauthorized intercept and access.",
    "decryption": "The reverse cryptographic process of converting encrypted ciphertext back into readable plain text format.",
    "vulnerability": "A security weakness, flaw, or misconfiguration in software that could be exploited by an unauthorized attacker.",
    "patch": "A software update released specifically to fix bugs, close security flaws, or correct system behavior.",
    "release": "A fully tested version of a software product formally distributed to end-users or deployed to live servers.",
    "version": "A unique identifier or number assigned to a specific state or release of software code (e.g., Semantic Versioning).",
    "commit": "A snapshot of staged changes saved to the version control repository history along with a descriptive message.",
    "branch": "An independent parallel line of development in version control isolating changes from the main codebase.",
    "merge": "To combine changes from one branch of version control directly into another target branch.",
    "conflict": "A state where Git cannot automatically resolve overlapping changes made to the exact same lines of code.",
    "pull request": "A formal submission in Git platforms asking team members to review and approve branch changes before merging.",
    "code review": "The systematic examination of source code by peer developers to find defects, ensure standards, and share knowledge.",
    "unit test": "An automated testing procedure verifying that a single, isolated function or component behaves exactly as expected.",
    "integration test": "An automated test verifying that multiple software modules, databases, or external APIs work together correctly.",
    "regression": "A software bug where previously working functionality breaks due to recent code changes or updates.",
    "mock": "A simulated object or API response used during automated testing to mimic real system behavior.",
    "timeout": "An event where a network request or execution process is canceled after exceeding its maximum allowed waiting time.",
    "retry": "An automated mechanism to re-attempt a failed network request or operation after a temporary error occurs.",
    "fallback": "An alternative backup procedure or secondary resource activated automatically when the primary system fails.",
    "bottleneck": "A specific component, database query, or resource constraint that limits the overall throughput of the entire system.",
    "scalability": "The capability of a software application to handle increased workload, traffic, and data volume gracefully.",
    "redundancy": "The duplication of critical hardware, servers, or database systems to ensure continuous uptime during failures.",
    "migration": "The systematic transfer of data, database schemas, or software applications from one environment or platform to another.",
    "schema": "The formal blueprint or structural definition organizing tables, columns, and relationships within a database.",
    "index": "A specialized database data structure created to drastically speed up query search and retrieval operations.",
    "transaction": "A logical unit of work containing multiple operations that must all succeed together or rollback completely (ACID).",
    "rollback": "To revert a database or software deployment back to its previous stable state after encountering an error.",
    "container": "A lightweight, standalone, executable software package bundling code, runtime, system tools, and libraries (e.g., Docker).",
    "microservice": "An architectural approach where a single application is built as a suite of small, loosely coupled, independently deployable services.",
    "monolith": "A traditional software architecture where all functional components of an application are tightly coupled into a single unified codebase.",
    "serverless": "A cloud execution model where the cloud provider automatically manages server provisioning, scaling, and execution on demand.",
    "pipeline": "An automated sequence of CI/CD build, testing, and deployment stages through which code changes flow from commit to production.",
    "artifact": "A compiled binary, executable package, or build file produced by an automated software compilation process.",
    "configuration": "The external settings, environment variables, and parameters controlling how a software application behaves in different environments.",
    "monitor": "To continuously track software metrics, server logs, and system health to detect anomalies and performance issues.",
    "alert": "An automated real-time notification triggered when system metrics or error rates cross predefined safety boundaries.",
    "metric": "A numerical measurement collected over time measuring system CPU usage, memory consumption, request rates, or latency.",
    "log": "An immutable chronological record of system events, application execution steps, warnings, and errors stored for analysis.",
    "exception": "An unexpected runtime event or condition that disrupts the normal execution flow of a software program.",
    "stack trace": "A detailed diagnostic list of active function calls and line numbers produced when an unhandled exception crashes a program.",
    "breakpoint": "A designated pausing spot in source code where a debugger stops execution so developers can inspect memory state.",
    "compile": "To translate human-readable source code into machine code or bytecode executed by a processor or virtual machine.",
    "runtime": "The active execution phase when a compiled or interpreted software application is actively running in memory.",
    "syntax": "The exact structural grammar, punctuation rules, and keyword definitions required by a programming language.",
    "semantics": "The intended computational meaning, logic, and operational behavior behind syntactic statements in source code.",
    "iterate": "To repeat a computational process or software enhancement cycle multiple times to refine results incrementally.",
    "iteration": "A single execution cycle within a loop or one distinct development sprint within an Agile methodology.",
    "sprint": "A set time-boxed period (typically 2 weeks) during which Agile engineering teams commit to delivering specific work items.",
    "agile": "An iterative, flexible software development philosophy emphasizing quick feedback cycles, cross-functional teams, and continuous delivery.",
    "scrum": "A structured Agile management framework utilizing daily standups, sprint planning, and retrospectives to organize team delivery.",
    "kanban": "A visual workflow management method using columns and cards to track tasks and limit work-in-progress continuously.",
    "backlog": "A prioritized master list of user stories, feature requests, technical debt, and bug fixes awaiting future development.",
    "stakeholder": "An individual, client, or department with a vested business interest in the outcome and features of a software project.",
    "milestone": "A significant scheduled checkpoint or completion date marking the end of a major project phase or release target.",
    "deliverable": "A tangible software build, feature, design document, or technical output promised to clients or management upon completion."
}

# Smart Contextual Definer for all remaining words
def generate_contextual_def(c):
    term = c.get('term', '').strip()
    vi = c.get('vi', '').split('|')[0].split('\u2014')[0].strip()
    pos = c.get('pos', '').strip()
    topic = c.get('topic', 'General').strip()
    example = c.get('example', '').strip()

    # Check exact match in CORE_DEFS
    term_lower = term.lower().strip()
    if term_lower in CORE_DEFS:
        return CORE_DEFS[term_lower]

    # Clean example without outer parentheses
    clean_ex = example
    if clean_ex.startswith('(') and clean_ex.endswith(')'):
        clean_ex = clean_ex[1:-1].strip()

    # If it's a phrase or sentence
    if len(term.split()) > 3 or pos in ['phr.', 'phrase'] or 'sentence' in topic.lower():
        if clean_ex and len(clean_ex) > 5 and clean_ex != term:
            return f"A professional English expression ({vi}) used in {topic} contexts. Example: \"{clean_ex}\""
        return f"A common workplace and professional English expression meaning '{vi}' in {topic} interactions."

    # If it's a phrasal verb or short idiom (2-3 words)
    if len(term.split()) in [2, 3] and ('v.' in pos or 'verb' in pos.lower() or pos == ''):
        if clean_ex and len(clean_ex) > 5:
            return f"A compound expression or phrasal verb meaning '{vi}' in {topic} and professional workflows. E.g., \"{clean_ex}\""
        return f"A professional phrasal verb or idiomatic expression indicating '{vi}' within {topic} contexts."

    # Single or short terms by part of speech
    if 'v.' in pos:
        base_def = f"To perform, execute, or carry out an action involving '{vi}' within {topic} and professional engineering environments."
    elif 'adj.' in pos:
        base_def = f"Describing a state, property, or characteristic relating to '{vi}' within software systems or business operations."
    elif 'adv.' in pos:
        base_def = f"An adverbial modifier expressing the manner or degree of '{vi}' during workplace communication or analysis."
    elif 'prep.' in pos or 'conj.' in pos:
        base_def = f"A relational or connecting grammatical word meaning '{vi}' used to structure professional statements."
    else: # n. or general
        base_def = f"A core concept, object, or professional terminology meaning '{vi}' commonly referenced in {topic} and IT discussions."

    if clean_ex and len(clean_ex) > 5 and clean_ex != term:
        base_def += f" (As used in: \"{clean_ex}\")"

    return base_def

def main():
    vocab_path = os.path.join(os.path.dirname(__file__), '..', 'vocab.json')
    vocab_path = os.path.abspath(vocab_path)
    print(f"Reading {vocab_path}...")

    with open(vocab_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cards = data.get('cards', [])
    print(f"Total cards found: {len(cards)}")

    updated_count = 0
    for c in cards:
        # Generate en_def if not present or empty
        if not c.get('en_def'):
            c['en_def'] = generate_contextual_def(c)
            updated_count += 1

    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated and updated en_def for {updated_count} cards!")

if __name__ == '__main__':
    main()
